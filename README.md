# Albert Sound Controller (Light Intensity Edition)

I’ve been seeing a bunch of reels, Shorts, TikToks, whatever, showcasing sound controllers from that old Reddit “contest” from like 10 years ago. The whole goal was to create the worst sound controller possible.

Even though I’m about a decade late, I decided to make my own.

This one is **light-intensity-based**.

It uses the light intensity detected by your webcam to control how loud the sound is:
- More light = louder sound  
- Pitch black = zero volume  

Simple. Dumb. Beautiful.

## Update: Rewritten in Python

I updated the Albert Sound Controller to be written in **Python** instead of Electron, because Electron fucking sucks.

It makes the app:
- Not truly portable  
- Over **500 MB** for absolutely no good reason  

Okay, there *is* a reason: Electron basically ships a whole Chrome browser with every app since it’s HTML and JavaScript based. Still, that’s insane.

So now it’s Python:
- A bit uglier  
- Actually portable  
- Barely weighs anything  

A trade-off I’ll gladly take.

## Running It

You can just run the already-built **EXE** to test it.

I don’t know why you would do that, but hey, it’s there.
