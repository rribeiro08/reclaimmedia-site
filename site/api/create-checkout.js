module.exports = async (req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
  
  if (!STRIPE_SECRET_KEY) {
    return res.status(500).json({ error: 'Stripe key not configured' });
  }

  try {
    const { email, name } = req.body;
    const origin = req.headers.origin || 'https://funnel-brown.vercel.app';

    // Use fetch directly instead of Stripe SDK
    const response = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'mode': 'payment',
        'customer_email': email,
        'line_items[0][price_data][currency]': 'usd',
        'line_items[0][price_data][unit_amount]': '2995',
        'line_items[0][price_data][product_data][name]': 'The Personal Agent Revolution',
        'line_items[0][price_data][product_data][description]': 'Complete Book + 3 Bonuses (PDF + EPUB)',
        'line_items[0][quantity]': '1',
        'success_url': `${origin}/course-upsell.html?session_id={CHECKOUT_SESSION_ID}`,
        'cancel_url': `${origin}/checkout.html`,
        'metadata[product]': 'personal-agent-revolution',
        'metadata[customer_name]': name || '',
      }).toString(),
    });

    const data = await response.json();

    if (data.error) {
      console.error('Stripe error:', data.error);
      return res.status(400).json({ error: data.error.message });
    }

    return res.status(200).json({ url: data.url });
  } catch (error) {
    console.error('Checkout error:', error.message);
    return res.status(500).json({ error: error.message });
  }
};
