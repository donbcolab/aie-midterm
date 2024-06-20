import chainlit as cl

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Description of Business",
            message="What is Airbnb's 'Description of Business'?",
            ),
        cl.Starter(
            label="Cash and cash equivalents",
            message="What was the total value of 'Cash and cash equivalents' as of December 31, 2023?",
            ),
        cl.Starter(
            label="Max shares 4Sale by Chesky",
            message="What is the 'maximum number of shares to be sold under the 10b5-1 Trading plan' by Brian Chesky?",
            ),
        ]
# ...
