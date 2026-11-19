# The Future Traveler

> **Dream it, remix it, have it, share it.**

The Future Traveler is HAX's mascot and its logo: a small red-helmeted time traveler with steampunk goggles, a lightbulb on a stalk named Eureka! and a green pack on his back. `WORLDVIEW.md` is what HAX believes and `VOICE.md` is how it sounds. This is the story the little guy in the corner of every HAX screen is telling, so everyone who draws him, writes about him or puts him in a bar tells the same one.

## His story

He went to the future and came back for the rest of us.

On the way he stopped in every era there has been. He did not go to look. He went to collect: the best ideas of each age, the ones worth keeping, and he put every one of them in his backpack. The engraver's patience. The poster's nerve. The arcade's joy. The early web's promise that anyone could have a page.

So the pack holds all of it: everything people have ever known and made. That is what he works with. Tell him your idea and he remixes all of human knowledge and creativity to bring it to life.

Then he hands it to you, and it is yours. Forever. Not rented, not locked in someone else's system, not gone when a company changes its mind. You own what you make.

That is HAX. With the right tools, you can build anything.

## You are a traveler too

He does not make the trip for you. He hands you his goggles.

Look through them and you see what he saw: a world where your ideas come to life. You can find anything. You can pull an idea down out of the air. When it lands, the bulb lights. That moment has a name: **Eureka!**

Then it goes in your backpack, and it goes where you go. To class. To the next job. To the other side of the world. Everywhere you travel you bring your ideas with you, and you keep having new ones, because you are seeing with the lenses HAX gave you.

That is why he is a traveler and not a wizard. A wand says the tool did something you could not. Goggles say you saw it yourself. We will build a better tomorrow because more people get to look.

## What each part of him means

Three parts of him are things you use. Each one does one job.

| Part | What it means | Your part in it |
| --- | --- | --- |
| The goggles | Seeing. He has seen the future, a place where data flows like water, and he lends you the view. | You put them on to search, to find anything and to see your idea before it exists. The lenses light when you look. |
| The lightbulb, **Eureka!** | The idea, at the moment it arrives. He carries it in front of him because it is the reason for the trip. | It lights when your idea lands. |
| The backpack | Keeping. His holds every idea he has collected, from every era. He draws on the past to build the future. | Yours holds everything you make. You own it forever and you can take it anywhere. |
| The red helmet with HAX across it | He wears the project's name. Wherever he shows up, HAX is there. | |

Eureka! is whatever light the era had. A candle in the steam age. A vacuum tube when radio was new. The glow of a picture tube in the 1980s. The idea is the same in every one; only the lamp changes.

## Why he changes

He is never drawn only one way, and that is on purpose.

A logo that can only look one way says "do not touch". Ours says the opposite: remix it. HAX is built so anything can be taken apart, mixed and made new, and that goes all the way down to the logo. He can be an 1880s engraving, a 1920s gold line drawing, a 1970s rainbow, a neon sign, four shades of green on a handheld screen, a terminal cursor. He is still him: helmet, goggles, bulb.

It also shows the method. He does not invent from nothing. He takes the great ideas of the past and builds the ideas of the future with them, which is what open standards, open source and open education have always done.

### Where to see it

- **The posters.** HAX's posters tell the story of the seven pillars once per era: steam age, modern marvel, roaring twenties, rainbow, corporate, cyberpunk, early web, the consoles and the World of Tomorrow, one poster to a pillar. They are in [haxtheweb/art](https://github.com/haxtheweb/art/tree/main/haxtheweb/posters).
- **The network bar.** At the right end of the bar on every HAX site, hover him and he tears through every era he has been to, then comes home to today. Click to remix: he stays in the era you chose. The eras are drawn in [`hax-future-traveler.js`](https://github.com/haxtheweb/webcomponents/blob/master/elements/hax-network-bar/lib/hax-future-traveler.js), one for each poster style, with the World of Tomorrow in every pillar's color. The same icons are kept as files to use anywhere, SVG and PNG, in [haxtheweb/art](https://github.com/haxtheweb/art/tree/main/future-traveler-eras).
- **The 36 variants.** He has been a paper cut, a sticker, a pixel sprite and plenty more, in [haxtheweb/art](https://github.com/haxtheweb/art/tree/main/future-traveler).

| Era | Drawn after |
| --- | --- |
| Today | The icon as it ships, `hax:future-traveler` |
| 1880s steam age | A sepia engraving with brass gears |
| 1900s modern marvel | Art nouveau in cream, teal and gold |
| 1920s roaring twenties | Black and gold deco with a sunburst |
| 1960s world of tomorrow | A travel poster, in the color of any one pillar |
| 1970s rainbow | One warm arch inside another |
| 1980s corporate | Built from stripes |
| 1980s cyberpunk | Nothing but neon |
| Handheld | Twelve pixels square, four greens |
| 1990s early web | A rainbow fill and a hard drop shadow |
| 32-bit | Flat-shaded polygons |
| Terminal | Green phosphor and a cursor |

## In the interface

The story is not decoration. It is how the parts of HAX are named.

- **The goggles are search and commands.** The palette that opens with `Alt+Shift` is drawn as his goggles, or as him wearing them, and the lenses light when it is active. Its written label is plain: "Search and commands". People who cannot see the goggles, or who use a screen reader, get the same clear name.
- **You call him with "Ok Future".** In voice mode that is the phrase that gets his attention, and when he answers, the card says **Future**. Nobody says "future" out loud by accident with "Ok" in front of it, and it says where we are headed.
- **Eureka! is the bulb.** It is a moment, not a place you go and not a name for the palette.
- **The backpack is where your sites live.** It fits the dashboard you land on when you sign in: the shelf of everything you have made and can carry off. That name is a direction, not yet a label in the product.
- **Merlin is the engineering name.** The palette was called Merlin and drawn as a wand. In code, schemas and architecture docs it still is: `<super-daemon>`, `merlin-schema`, a "Merlin program". Nothing a person reads on screen or hears from the voice says Merlin or shows a wand (see the mascot rule in `RULES.md`).

## Using him

- **Call him the Future Traveler.** Always, in writing. Older names are retired (see the mascot rule in `RULES.md`). Out loud, to get his attention, he answers to "Ok Future". People will also call him "HAX" or "the HAX guy", and that is fine: he wears the name.
- **Keep him on-model.** Any era, any medium, but always the helmet with HAX on it, the goggles and the lightbulb. The pack is there even when the drawing is too small to show it.
- **Short form is the goggles.** When there is no room for all of him, draw the two lenses. Do not use a lightbulb alone to stand for HAX: a bulb by itself means "tip" everywhere else.
- **He sits top right.** In every HAX interface he is in the top right corner. He represents HAX there.
- **Playful, never snarky.** He is fun, a bit silly, and on a mission to bring the rest of us along.
- **A new era is welcome.** Draw him the way a time or a movement would have, goggles and lamp included. Add it to the eras file and to the art repo, and say which era it is.

*WE ARE… HAXTheWeb.*
