const Stripe = require('stripe');

if (!process.env.STRIPE_SECRET_KEY) {
  console.error('STRIPE_SECRET_KEY not set');
}

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || 'sk_test_missing');

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(200, corsHeaders);
    res.end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  Object.entries(corsHeaders).forEach(([key, value]) => {
    res.setHeader(key, value);
  });

  try {
    const { email, name, paymentMethodId } = req.body;

    if (!email || !name || !paymentMethodId) {
      return res.status(400).json({
        error: 'Required fields: email, name, paymentMethodId',
      });
    }

    // Amount: $29.95 for book + bonuses
    const chargeAmount = 2995;

    // Find or create customer
    let customer;
    const existingCustomers = await stripe.customers.list({
      email: email.toLowerCase().trim(),
      limit: 1,
    });

    if (existingCustomers.data.length > 0) {
      customer = existingCustomers.data[0];
      if (customer.name !== name) {
        customer = await stripe.customers.update(customer.id, { name });
      }
    } else {
      customer = await stripe.customers.create({
        email: email.toLowerCase().trim(),
        name,
        metadata: {
          source: 'openclaw-book-funnel',
          first_product: 'personal-agent-revolution',
        },
      });
    }

    // Attach payment method
    await stripe.paymentMethods.attach(paymentMethodId, {
      customer: customer.id,
    });

    // Set as default
    await stripe.customers.update(customer.id, {
      invoice_settings: {
        default_payment_method: paymentMethodId,
      },
    });

    // Create and confirm PaymentIntent
    const paymentIntent = await stripe.paymentIntents.create({
      amount: chargeAmount,
      currency: 'usd',
      customer: customer.id,
      payment_method: paymentMethodId,
      confirm: true,
      description: 'The Personal Agent Revolution (Book + Bonuses)',
      metadata: {
        product: 'personal-agent-revolution',
        customer_email: email,
        customer_name: name,
      },
      return_url: req.headers.referer || 'https://reclaimmedia.com/thank-you-book',
      automatic_payment_methods: {
        enabled: true,
        allow_redirects: 'never',
      },
    });

    if (paymentIntent.status === 'succeeded') {
      return res.status(200).json({
        success: true,
        customerId: customer.id,
        paymentMethodId: paymentMethodId,
        paymentIntentId: paymentIntent.id,
      });
    } else if (paymentIntent.status === 'requires_action') {
      return res.status(200).json({
        success: false,
        requires_action: true,
        client_secret: paymentIntent.client_secret,
        customerId: customer.id,
        paymentMethodId: paymentMethodId,
      });
    } else {
      return res.status(400).json({
        error: 'Payment not completed. Status: ' + paymentIntent.status,
      });
    }
  } catch (error) {
    console.error('Payment error:', error.message, error.type, error.code);

    if (error.type === 'StripeCardError') {
      return res.status(400).json({
        error: error.message || 'Card declined. Please check your details and try again.',
      });
    }

    if (error.type === 'StripeAuthenticationError') {
      return res.status(500).json({
        error: 'Stripe API key mismatch. Check test/live mode.',
      });
    }

    return res.status(500).json({
      error: error.message || 'Internal server error. Please try again.',
    });
  }
};
