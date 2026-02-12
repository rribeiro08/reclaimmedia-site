// Stripe Webhook Handler
// Listens for successful payments and provisions user access in Supabase

const crypto = require('crypto');

// Products and their access levels
const PRODUCTS = {
  'personal-agent-revolution': { type: 'book', hasCoursesAccess: false },
  'personal-agent-revolution-course': { type: 'course', hasCoursesAccess: true },
  'personal-agent-revolution-bundle': { type: 'bundle', hasCoursesAccess: true }
};

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, stripe-signature');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET;
  const SUPABASE_URL = process.env.SUPABASE_URL;
  const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY; // Service role key for admin operations

  if (!STRIPE_WEBHOOK_SECRET || !SUPABASE_URL || !SUPABASE_SERVICE_KEY) {
    console.error('Missing required environment variables');
    return res.status(500).json({ error: 'Server configuration error' });
  }

  try {
    // Get the raw body
    const rawBody = typeof req.body === 'string' ? req.body : JSON.stringify(req.body);
    const signature = req.headers['stripe-signature'];

    // Verify webhook signature
    const event = verifyStripeSignature(rawBody, signature, STRIPE_WEBHOOK_SECRET);

    console.log('Received Stripe event:', event.type);

    // Handle checkout.session.completed event
    if (event.type === 'checkout.session.completed') {
      const session = event.data.object;
      
      // Extract customer info
      const email = session.customer_email || session.customer_details?.email;
      const customerName = session.customer_details?.name || session.metadata?.customer_name;
      const paymentId = session.payment_intent || session.id;
      const product = session.metadata?.product || 'personal-agent-revolution';
      
      if (!email) {
        console.error('No email found in session:', session.id);
        return res.status(400).json({ error: 'No customer email' });
      }

      console.log('Processing purchase for:', email, 'Product:', product);

      // Determine access level
      const productInfo = PRODUCTS[product] || { type: 'book', hasCoursesAccess: false };

      // Create/update user in Supabase
      await provisionAccess({
        email: email.toLowerCase(),
        name: customerName,
        paymentId,
        product,
        hasCourseAccess: productInfo.hasCoursesAccess,
        supabaseUrl: SUPABASE_URL,
        supabaseKey: SUPABASE_SERVICE_KEY
      });

      console.log('Access provisioned for:', email);

      // Send welcome email (optional - implement with your email provider)
      // await sendWelcomeEmail(email, customerName, product);

      return res.status(200).json({ received: true, email, product });
    }

    // Handle payment_intent.succeeded (backup)
    if (event.type === 'payment_intent.succeeded') {
      const paymentIntent = event.data.object;
      const email = paymentIntent.receipt_email;
      
      if (email) {
        console.log('Payment succeeded for:', email);
        // Could provision access here as backup
      }
    }

    // Acknowledge other events
    return res.status(200).json({ received: true });

  } catch (error) {
    console.error('Webhook error:', error.message);
    return res.status(400).json({ error: error.message });
  }
};

// Verify Stripe webhook signature
function verifyStripeSignature(payload, signature, secret) {
  if (!signature) {
    throw new Error('No Stripe signature provided');
  }

  const parts = signature.split(',').reduce((acc, part) => {
    const [key, value] = part.split('=');
    acc[key] = value;
    return acc;
  }, {});

  const timestamp = parts['t'];
  const expectedSignature = parts['v1'];

  if (!timestamp || !expectedSignature) {
    throw new Error('Invalid signature format');
  }

  // Check timestamp (prevent replay attacks)
  const tolerance = 300; // 5 minutes
  const now = Math.floor(Date.now() / 1000);
  if (now - parseInt(timestamp) > tolerance) {
    throw new Error('Webhook timestamp too old');
  }

  // Compute expected signature
  const signedPayload = `${timestamp}.${payload}`;
  const computedSignature = crypto
    .createHmac('sha256', secret)
    .update(signedPayload)
    .digest('hex');

  // Compare signatures
  if (computedSignature !== expectedSignature) {
    throw new Error('Invalid signature');
  }

  return JSON.parse(payload);
}

// Provision access in Supabase
async function provisionAccess({ email, name, paymentId, product, hasCourseAccess, supabaseUrl, supabaseKey }) {
  // Check if purchase already exists
  const checkResponse = await fetch(
    `${supabaseUrl}/rest/v1/purchases?email=eq.${encodeURIComponent(email)}&stripe_payment_id=eq.${encodeURIComponent(paymentId)}`,
    {
      method: 'GET',
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json'
      }
    }
  );

  const existingPurchases = await checkResponse.json();
  
  if (existingPurchases && existingPurchases.length > 0) {
    console.log('Purchase already exists for:', email);
    return;
  }

  // Insert new purchase record
  const insertResponse = await fetch(`${supabaseUrl}/rest/v1/purchases`, {
    method: 'POST',
    headers: {
      'apikey': supabaseKey,
      'Authorization': `Bearer ${supabaseKey}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=minimal'
    },
    body: JSON.stringify({
      email,
      customer_name: name || null,
      stripe_payment_id: paymentId,
      product,
      has_course_access: hasCourseAccess,
      access_granted: true,
      purchased_at: new Date().toISOString()
    })
  });

  if (!insertResponse.ok) {
    const error = await insertResponse.text();
    throw new Error(`Supabase insert failed: ${error}`);
  }

  // Create auth user if they don't exist
  try {
    const createUserResponse = await fetch(`${supabaseUrl}/auth/v1/admin/users`, {
      method: 'POST',
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email,
        email_confirm: true,
        user_metadata: {
          name: name || null,
          product,
          has_course_access: hasCourseAccess
        }
      })
    });

    if (createUserResponse.ok) {
      console.log('Created auth user for:', email);
    } else {
      // User might already exist, which is fine
      const error = await createUserResponse.json();
      if (!error.message?.includes('already')) {
        console.warn('Could not create auth user:', error);
      }
    }
  } catch (e) {
    console.warn('Auth user creation error (non-fatal):', e.message);
  }
}
