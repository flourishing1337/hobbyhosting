import type { NextApiRequest, NextApiResponse } from "next";
import Stripe from "stripe";

const stripeSecret = process.env.STRIPE_SECRET_KEY;
const stripe = stripeSecret
  ? new Stripe(stripeSecret, { apiVersion: "2023-10-16" })
  : null;

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    res.status(405).end("Method Not Allowed");
    return;
  }

  if (!stripe) {
    res.status(500).json({ error: "Stripe not configured" });
    return;
  }

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      mode: "payment",
      line_items: [
        {
          price_data: {
            currency: "usd",
            unit_amount: 50000,
            product_data: { name: "We film your business" },
          },
          quantity: 1,
        },
      ],
      success_url: `${req.headers.origin}/film?success=true`,
      cancel_url: `${req.headers.origin}/film?canceled=true`,
    });

    res.status(200).json({ url: session.url });
  } catch {
    res.status(500).json({ error: "Failed to create session" });
  }
}
