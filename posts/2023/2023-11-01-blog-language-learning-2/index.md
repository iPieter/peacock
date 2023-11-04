Now that we have an idea of the functionality of the app, it's time to get started. Since we have React Native bindings for Whisper, let's use React Native. I have [some experience](https://github.com/iPieter/chat_app) with that, so that's handy.

The first question is how your app will actually function and what the user flow will be. I think the most natural UI would be something similar to a chat conversation, since we want our users to hold a (short) conversation with the language model.

![screenshot.png](screenshot.png)

Thanks to my high quality wireframe, I now know what to build: a chat app. 
For an app that will focus on conversations, I think that is the most natural UI.
The user first selects a topic (e.g. 'Coffee') based on an input (as in the figure) or based on a set of predefined topics, as is the plan with topic modeling.


# Planning
So now that have have some basic expectations, a set of technologies (see blogpost of day 1) and a concrete idea, let's start planning.


## Backend
The backend of this application is pretty rudimentary; we need an endpoint to get the newest response to a conversation about a topic and another endpoint to get corrections for each user response.

## App
The app itself is also quite basic, since it is only a chat screen about a certain topic. The most challenging aspect is integrating TTS and STT nicely, although the smaller Whisper models run pretty reliably on iOS at least.

The rest of this day was wasted setting up React Native. Turns out that there were some functions renamed in RN 62.0 and not every library was updated yet. Fun.
