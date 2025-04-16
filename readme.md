# Assignment Submission

## GitHub Repository Link
[Link to Your GitHub Repository](https://github.com/rajeevalahari/is601homework10-spring2025)

### Resolved Issues:

- **[Issue #1: Username Validation](https://github.com/rajeevalahari/is601homework10-spring2025/tree/1-username-validationreject-invalid-nicknames)**
  - **Problem:** Usernames shorter than 3 characters, containing spaces or emojis were incorrectly allowed.
  - **Solution:** Updated validation logic in Pydantic schema with regex constraints (`pattern`) to enforce length and character restrictions. Implemented comprehensive pytest cases covering edge scenarios.

- **[Issue #2: Username Uniqueness](https://github.com/rajeevalahari/is601homework10-spring2025/tree/3-ensure-nickname-uniqueness-at-the-db-and-service-layer)**
  - **Problem:** Duplicate nicknames were permitted, causing database conflicts.
  - **Solution:** Added uniqueness check in user creation and update logic at service and database layers, supplemented by test cases that verify rejection of duplicate nicknames.

- **[Issue #3: Password Validation](https://github.com/rajeevalahari/is601homework10-spring2025/tree/5-issue3-password-validation)**
  - **Problem:** Weak passwords (without complexity requirements) were accepted.
  - **Solution:** Enhanced validation rules to require a minimum of 8 characters, including at least one uppercase letter, one lowercase letter, one digit, and one special character. Verified through automated tests.

- **[Issue #4: Profile URLs Validation](hhttps://github.com/rajeevalahari/is601homework10-spring2025/tree/7-profile-urls-validation)**
  - **Problem:** Profile URLs accepted invalid or non-http(s) formats.
  - **Solution:** Added regex-based URL validation in the schema to ensure URLs start with `http://` or `https://`. Tests were written to validate correct handling of URL formats.

- **[Issue #5: Empty Body PUT Request Handling](https://github.com/rajeevalahari/is601homework10-spring2025/tree/9-profile-update-must-fail-if-body-empty)**
  - **Problem:** The PUT `/users/{id}` endpoint incorrectly allowed empty request bodies.
  - **Solution:** Implemented a root validator in the schema to reject requests with empty bodies, supported by integration tests to ensure correct error responses.

- **[Issue #6: Schema Example Data Consistency](https://github.com/rajeevalahari/is601homework10-spring2025/tree/11-fixed-example-values)**
  - **Problem:** Schema example data were mutable and changes went unnoticed in tests.
  - **Solution:** Developed dedicated pytest cases that assert fixed example values for schema fields, ensuring changes in schema examples break tests and are immediately noticeable.

## Dockerhub Deployment
[Link to Project Docker Image](https://hub.docker.com/r/rajeevalahari/event_manager)

## Reflection
Throughout this assignment, I gained valuable insights into REST API development, especially the importance of robust validation mechanisms and comprehensive testing strategies. Addressing username and password validation taught me best practices in data security and integrity, while handling edge cases in profile updates reinforced the need for thorough API testing. Working on schema consistency underscored the value of maintaining documentation aligned with actual implementation.

Collaboration via GitHub, branching, pull requests, and code reviews significantly improved my ability to produce clean, maintainable code. Engaging in detailed debugging and resolving issues enhanced my understanding of effective troubleshooting techniques. Overall, the assignment has provided a solid foundation in secure, test-driven API development and collaborative software engineering practices.

