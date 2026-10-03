# Enterprise Demo Application

This repository contains a small e-commerce application used for
demonstrating repository-level code understanding.

The application supports:

- Creating customer orders
- Processing orders through checkout
- Applying discounts for premium users
- Processing payments
- Validating payment amounts

## Main Application Flow

An order enters the checkout workflow.

Checkout determines the applicable price and then sends the
resulting amount to the payment system.

The repository also contains automated tests and architecture
documentation describing the application's overall design.

## Repository Structure

- `app/` — application source code
- `tests/` — automated tests
- `docs/` — architecture documentation