import { Basket } from '../src/basket.js';

// The scenarios use pounds. Checkout's public operations use integer pence.
export class CheckoutDriver {
  constructor(eligiblePounds) {
    this.basket = new Basket(eligiblePounds * 100);
  }

  applyPromotion(code) {
    this.basket.applyPromotion(code);
  }

  totalInPounds() {
    return this.basket.totalInPence() / 100;
  }
}
