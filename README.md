# Chatbot

# container

The only strictly required tools for this environment are docker and
docker-compose. The mechanisms of installing those varies vastly across
operating systems. We recommend that you use Docker for Desktop if you can
use it freely, or use Rancher Desktop with nerdctl otherwise.

This is the most isolated environment, and everything happens within a
container. The advantage of an isolated environment is that it avoids
the "works in my machine" problem.

# Cluster

If you are using your ops hat, this is where you will spend time testing your
yamls. We will work with a k8s cluster, usually one locally created with kind,
and we will stitch the services together. For commands in this enviroment
you need running kubernetes cluster. We recommend using kind to create one.

`kind create cluster -n chatbot`

### preview

The preview environment is capable of building the full code and bringing
up any services. It is orchestrated by skaffold, which builds the code
with increased hermeticity, and brings up all services by default. Deployment
is fully isolated through the usage of a local kubernetes cluster. The preview
enviroment is brought up with the commands belows. You can run

`cd products/chatbot`
`skaffold dev -p preview`

This will bring the full app.This setup is better suited for debugging
integration problems spawning several components and for executing functional
tests. It can also power a pristine QA environment or serve as a simple way of
sharing private development results. Services within preview are shared.

Note: For testing or sharing purposes, you might need ngrok to expose your
local services to the internet, it is only needed due to security purposes.

To start ngrok without fixed domain you can use this in ngrok.yaml:

`args: - "http" - "chat-app:8000"`

Grabbing the Public URL: After starting ngrok, you can grab the dynamically
assigned public domain with:

`curl -s http://localhost:4040/api/tunnels | jq '.tunnels[0].public_url'`

Fixing a Custom Domain: To use a fixed custom domain instead of a dynamic one,
go to the ngrok console and acquire a domain. Then, update the ngrok.yaml
file to call ngrok with the fixed domain:

`args: -"http" - "--url=your-ngrok-domain.ngrok-free.app" - "chat-app:8000"`

Code in the preview environment should be fully optimized.

# Backend development

The backend development is done using the FastAPI , Python and Whatspp Business
Api. The main service lives in /services/chatbot.
