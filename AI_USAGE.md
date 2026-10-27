AI Usage Documentation

1. AI Tools Used

AI tool: ChatGPT

Purpose: To understand the assignment requirements, troubleshoot errors, review the box recommendation logic, and get guidance on Django testing and API verification.

2. Prompts Given

The prompts I used during development included requests for help with:

Understanding the assignment requirements and planning the Django project.

Implementing and testing the box recommendation service.

Troubleshooting Django shell and API issues.

Understanding test failures and correcting the test setup.

Verifying API responses and error handling.

These are summaries of my prompts. The actual prompts and conversation are available in the exported chat transcript.

3. Output Accepted

I used AI suggestions as guidance for understanding and testing the application, including:

Checking whether the recommended box satisfies the product dimensions and weight requirements.

Testing the recommendation API with valid, empty, and nonexistent orders.

Understanding Django test failures and reviewing the expected behavior.

Running automated tests to verify the implementation.

I reviewed the suggestions against the project requirements before applying changes.

4. Output Rejected or Modified

I did not assume that every AI suggestion was correct. I reviewed the proposed changes against the actual code and test results.

For example, when the rotation test failed because the service selected the Small box instead of the expected Medium box, I inspected the test data and box dimensions. I then modified the test setup so that the Small box could not accommodate the product.

5. Mistakes Found During AI-Assisted Development

One important issue was the expected result in the product rotation test. The original product dimensions could fit inside the Small box after rotation, so the service selected the cheaper Small box instead of Medium.

The test expectation did not match the available box dimensions. After modifying the test setup, the complete test suite passed with 9 tests.

6. Verification of Final Code

I verified the implementation using the following steps:

Ran the Django development server.

Sent a POST request to the box recommendation endpoint for an order containing an item.

Checked that the API returned the recommended box and recommendation_saved: true.

Tested an empty order and verified that the API returned HTTP 422 with an appropriate error message.

Ran python manage.py test.

Confirmed that all 9 tests passed and Django reported no system-check issues.

7. Limitations

The recommendation service checks product dimensions, total order volume, and total weight. These checks do not guarantee that multiple products can always be physically packed together in a box. A complete three-dimensional packing algorithm would be needed to handle that problem reliably.