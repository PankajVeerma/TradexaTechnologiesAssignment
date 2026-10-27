est Cases

Overview

The project includes automated tests for box recommendation logic and API behavior.

Test Case List

Test Case                   Scenario                                            Expected Result

TC-01                     Select a box for an order containing a product     The cheapest suitable box is selected

TC-02                     Small box has insufficient weight capacity         A suitable alternative box is selected

TC-03                     All available boxes have insufficient weight capacity    NoSuitableBoxError is raised

TC-04                     Order contains no items                                 NoSuitableBoxError is raised

TC-05                     Product dimensions fit after rotation                   A suitable box is selected

TC-06                     Product data validation                                 Invalid dimension or weight values are rejected

TC-07                     API receives a valid order ID                           Recommended box details are returned and saved

TC-08                     API receives an empty order                             HTTP 422 is returned

TC-09                     API receives a nonexistent order ID                     HTTP 404 is returned




Run the following command from the directory containing manage.py:     python manage.py test