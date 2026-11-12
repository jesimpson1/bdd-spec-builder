export class Basket {
  constructor(eligibleSubtotalPence) {
    this.eligibleSubtotalPence = eligibleSubtotalPence;
    this.discountPence = 0;
  }

  applyPromotion(code) {
    if (code === 'SAVE10') {
      this.discountPence = Math.round(this.eligibleSubtotalPence * 0.10);
    }
  }

  totalInPence() {
    return this.eligibleSubtotalPence - this.discountPence;
  }
}
