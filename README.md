# What

A simple project demonstrating how to build a web app that uses an island architecture. The advantages are client-side interactiveness while preserving serverside features. Here's what each component demonstrates:

1. Counter: HTMX island
2. UserTable: server-rendered island
3. Flow: React island

## Pros

- Allows you to avoid the complexities of keeping two applications (frontend-backend) in sync - in other words: no DTOs, no entity boilerplate, etc.
- Islands are largely tech-agnostic - as long as the underlying tech can interact with HTML.
- Much lighter than framework based approaches.
- Provides the safety of a serverside application.
- No framework black-box abstractions.

## Cons

- Some setup is required for writing new applications - installing tailwind, configuring javascript builds, making FastAPI serve static files.
- No frameworks approach means there's a learning curve (even if it is much smaller than learning frameworks) - you have to make your own (ideally good) rules.
- Utilizing parts of existing frameworks is possible, but requires deeper knowledge.

### Running

1. `npm install`
2. `npm run build`
3. `python ./main.py`

# Issues

⚠️ In the current implementation, changes to Javascript files require a full rebuild of the containers. To change that, we'd need to improve the container so that python and Node are available in the same image.
