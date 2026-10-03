# Application Architecture

The application processes customer orders through a checkout workflow.

When an order is created, the order flow enters the checkout process.
Checkout calculates the applicable price adjustment before sending the
resulting amount to the payment system.

The payment system validates the payment amount before accepting it.

The application also contains tests covering order creation and checkout
behavior.
