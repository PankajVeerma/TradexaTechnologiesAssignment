# TradexaTechnologiesAssignment

Box Selection System

Overview

The Box Selection System is a Django REST Framework application that recommends a suitable shipping box for an ecommerce order.

The system considers product dimensions, total order weight, total product volume, and box cost to select the cheapest box that satisfies its current validation rules.

Features

Manage products with dimensions and weight.

Manage shipping boxes with internal dimensions, maximum weight capacity, and cost.

Create orders containing one or more products and quantities.

Recommend a suitable shipping box for an order.

Save the recommended box against the order.

Handle empty orders and nonexistent order IDs.

Validate product and box data.

Run automated tests for the recommendation service and API.

Technology Stack

Python
Django
Django REST Framework
SQLite or the database configured in Django settings
Django automated testing framework

Project Structure
boxSelectionSystem/
├── config/
├── products/
├── boxes/
├── orders/
│   ├── services.py
│   ├── tests.py
│   └── ...
├── manage.py
├── requirements.txt
├── README.md
└── AI_USAGE.md

Setup Instructions

1. Clone the repository

git clone <GITHUB_REPOSITORY_URL>
cd boxSelectionSystem

Replace <GITHUB_REPOSITORY_URL> with your actual GitHub repository URL.

2. Create and activate a virtual environment

Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

If a requirements file has not yet been created, install the project's required Django and Django REST Framework dependencies and generate the file before submitting.

4. Apply database migrations

python manage.py migrate

5. Start the development server

python manage.py runserver

The local development server runs at:

http://127.0.0.1:8000/

API Endpoints

List products

Method: GET

/api/products/

Returns the products available in the system.

List shipping boxes

Method: GET

/api/boxes/

Returns the available shipping boxes, ordered by cost and ID.

Recommend a box for an order

Method: POST

/api/orders/<order_id>/recommend-box/

Example request:

POST http://127.0.0.1:8000/api/orders/4/recommend-box/

No request body is required for this endpoint.

Example successful response:

{
  "order_id": 4,
  "recommended_box": {
    "id": 2,
    "name": "Medium",
    "length": "20.00",
    "width": "15.00",
    "height": "10.00",
    "max_weight": "5.00",
    "cost": "15.00"
  },
  "recommendation_saved": true
}

The response values above are an example from local testing. Actual values depend on the records in the database.

Box Recommendation Logic

The recommendation service performs the following checks:

Rejects an order that contains no items.

Calculates the total weight of the order using each product's weight and quantity.

Calculates the total product volume.

Checks each box's maximum weight capacity.

Checks whether the total product volume fits within the box's internal volume.

Checks whether each individual product fits inside the box, allowing rotation by comparing sorted dimensions.

Selects the lowest-cost box among the boxes that pass these checks.

Raises an error if no suitable box is found.

The API saves the selected box in the database as the order's recommendation.

Error Handling

Scenario                                      Expected HTTP status
Recommendation succeeds                         200

Order does not exist                            404

Order contains no items                         422

No suitable box is available                    422

The exact response body depends on the API's error-handling implementation.

Running Tests

Run the automated test suite with:     python manage.py test

During development, the test suite reported:
Found 9 test(s).
Ran 9 tests
OK

Django also reported no system-check issues in that run.

Assumptions and Limitations

Product dimensions and box dimensions use the same unit of measurement.

Product weight and box maximum weight use the same unit of measurement.

Box cost is used to choose the cheapest box among eligible candidates.

Product rotation is supported by comparing sorted dimensions.

Total order volume and total weight are checked independently.

The current implementation does not perform full three-dimensional packing of multiple products. Therefore, passing the volume and individual-product checks does not guarantee that every item can physically fit together inside one box.

Authentication and production deployment configuration depend on the final project requirements.

AI Usage Disclosure

AI assistance was used during development for understanding requirements, troubleshooting, reviewing test failures, and verifying API behavior.

See AI_USAGE.md for details about the tools used, prompts, accepted or modified suggestions, mistakes identified, and verification steps.

License

This project was developed as a technical assignment. No license has been specified.





--------------------What I Learned:

While working on this assignment, I learned how to structure a Django project using different models. I understood how Product and Box store information such as dimensions and weight, and how Order and OrderItem are connected to represent the products in an order.

I also learned how to build a box recommendation service that checks product dimensions, total weight, volume, and box cost before selecting the cheapest suitable box.

During testing, I faced an issue with my rotation test because the Small box could fit the product after rotation, but my test expected the Medium box. This helped me understand the importance of checking test data and expected results carefully.

I also learned how to test API responses for different situations. I verified that a valid order returns a box recommendation, an empty order returns HTTP 422, and a nonexistent order returns HTTP 404.

If I improve this project in the future, I would like to implement a proper 3D packing algorithm to check whether multiple products can physically fit together inside a box.