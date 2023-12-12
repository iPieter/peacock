# Conversations and corrections
This works pretty well: GPT-3.5 and GPT-4 both respond in a nice way and stays on topic.
The only challenge is that I want a structured output that contains the response, but also a suggested response to that. I could split this up, but I want to keep the number of calls (and tokens) to a minimum.

With the corrections, this issue is even larger. I do want to get a lot of metadata about the types of mistakes a user makes, but GPT-3.5 keeps ignoring some of the instructions. Especially providing a table (in markdown format) with the correct conjugation of a verb is challenging. GPT-4 generates that without a problem though.

## Controllable text generation
Since we have a predefined structure for our output, let's use [Guidance](https://github.com/guidance-ai/guidance) from Microsoft. This library allows us to generate only the parts of our prompt that we need and we have a more structured output, without explicitly prompting GPT to do that.

  <figure>
    <div class="col-md-10 col-sm-10 col-10 mx-auto"> 
        <img src="prompt.png" width="100%" alt="Prompt for the corrected sentences."/>
        </div>
  </figure>


Now that that prompt works, we can throw it in a Django backend and point our app to it. The idea would be that the number of mistakes are shown and the explanation could then be rendered in a separate screen.

# The basic layout
This is not much yet, but we do have a basic conversational screen. The app correctly calls the backend for a new response and keeps track of the old ones. The number of mistakes will be added on the right side of the messages by the user.

  <figure>
    <div class="col-md-6 col-sm-8 mx-auto"> 
        <img src="screenshot.jpg" width="100%" alt="Screenshot of the basic functionality."/>
        </div>
  </figure>
