import assert from 'node:assert/strict';
import { Given, When, Then } from '@cucumber/cucumber';
import { CheckoutDriver } from './checkout-driver.js';

Given('my basket contains £{int} of goods eligible for SAVE10', function (pounds) {
  this.checkout = new CheckoutDriver(pounds);
});

When('I apply the {word} promotion', function (code) {
  this.checkout.applyPromotion(code);
});

Then('my basket total is £{int}', function (expectedPounds) {
  assert.equal(this.checkout.totalInPounds(), expectedPounds);
});
