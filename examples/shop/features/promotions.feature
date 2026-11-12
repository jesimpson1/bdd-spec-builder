Feature: Basket promotions
  SAVE10 gives shoppers 10% off eligible goods.

  Scenario: Applying SAVE10 to an eligible basket
    Given my basket contains £80 of goods eligible for SAVE10
    When I apply the SAVE10 promotion
    Then my basket total is £72
