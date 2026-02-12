// Get customer email from Stripe checkout session
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const sessionId = req.query.session_id;
  
  if (!sessionId) {
    return res.status(400).json({ error: 'session_id required' });
  }

  const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
  
  if (!STRIPE_SECRET_KEY) {
    return res.status(500).json({ error: 'Stripe not configured' });
  }

  try {
    const response = await fetch(`https://api.stripe.com/v1/checkout/sessions/${sessionId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${STRIPE_SECRET_KEY}`,
      },
    });

    if (!response.ok) {
      return res.status(404).json({ error: 'Session not found' });
    }

    const session = await response.json();
    
    // Return only the email, nothing sensitive
    const email = session.customer_email || session.customer_details?.email;
    
    if (email) {
      return res.status(200).json({ email });
    } else {
      return res.status(404).json({ error: 'No email found' });
    }
  } catch (error) {
    console.error('Get session error:', error.message);
    return res.status(500).json({ error: error.message });
  }
};
