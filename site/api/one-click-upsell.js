const Stripe = require('stripe');

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

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
    const { customerId, paymentMethodId } = req.body;

    if (!customerId || !paymentMethodId) {
      return res.status(400).json({
        error: 'Required fields: customerId, paymentMethodId',
      });
    }

    // Verify customer
    const customer = await stripe.customers.retrieve(customerId);
    if (!customer || customer.deleted) {
      return res.status(400).json({
        error: 'Customer not found.',
      });
    }

    // One-click charge for Agent Mastery Course ($97 = 9700 cents)
    const paymentIntent = await stripe.paymentIntents.create({
      amount: 9700,
      currency: 'usd',
      customer: customerId,
      payment_method: paymentMethodId,
      confirm: true,
      off_session: false,
      description: 'Agent Mastery Course — Complete Companion to The Personal Agent Revolution',
      metadata: {
        product: 'agent-mastery-course',
        upsell: 'true',
        customer_email: customer.email,
      },
      return_url: 'https://reclaimmedia.com/thank-you-full',
      automatic_payment_methods: {
        enabled: true,
        allow_redirects: 'never',
      },
    });

    if (paymentIntent.status === 'succeeded') {
      return res.status(200).json({
        success: true,
        paymentIntentId: paymentIntent.id,
      });
    } else if (paymentIntent.status === 'requires_action') {
      return res.status(200).json({
        success: false,
        requires_action: true,
        client_secret: paymentIntent.client_secret,
      });
    } else {
      return res.status(400).json({
        error: 'Payment not completed. Status: ' + paymentIntent.status,
      });
    }
  } catch (error) {
    console.error('Upsell payment error:', error);

    if (error.type === 'StripeCardError') {
      return res.status(400).json({
        error: error.message || 'Card declined. Please try again.',
      });
    }

    return res.status(500).json({
      error: 'Error processing payment. Please try again.',
    });
  }
};
