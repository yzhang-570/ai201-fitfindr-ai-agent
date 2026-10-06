# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

target - measurable (number, count, or rate) via observation, criterion NOT opinion
why this target - why not stricter/why this target, must mention tools, loop, or data (listings, wardrobe)

---

criterion:
- 1. happy path: loop proceeds and completes all tools calls expected - when branch is successful
     - expected fields in state are non-empty
- 2. unhappy path: loop never proceeds or completes 2nd and 3rd tool calls - when branch is unsuccessful
- 3. tool calls receive correct inputs
     - fields in state contain expected/matching content (selected item is present in outputs of both tool calls - suggested_outfit and fit_card)
- 4. happy path: fit cards are generated with content from selected item - when branch is successful
     - fit cards contain the selected item's price
- 5. search parses queries and applies max price filter correctly
     - selected item must be under the max price specified by the user's query

Q: if the criteria itself has a condition for the test
(ex. a matching query - aka. a search that returns at least one listing)
(ex. an impossibly query - aka. a search that returns an empty list)

should evaluations ONLY consider test cases that satisfy the initial condition when determining if the criteria was met?


## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 5 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. 
     
     no, if missed, then the listings would be empty - at least one listig means keyword match was successful-->
     Loop and tool (failure case design): Assuming that search_listings() succeeds in returning at least one listing, the branch (in the loop) will always be fulfilled and proceed to the other two tools.

     The tools have clearly defined failure cases that should never block the sequence of calls even if they receive nothing. (suggest_outfit returns generic styling advice for item instead of specific outfit if empty wardrobe, create_fit_card describes the item if no outfit is passed).

     **Therefore, all three tool calls should always be completed as long as the branch is fulfilled (list returned from list isn't empty).

     Observable: Check that selected_item, outfit_suggestion, and create_fit_card all not empty.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
     Loop (branch): This is the exact definition of the failure branch. The loop's branch condition should **always** returns and writes a message (error field) when the search returns an empty list, meaning it will never call suggest_outfit() or create_fit_card().

     Observable: search_results, selected_item, outfit_suggestion, and create_fit_card should all be empty, and error must contain a messsage naming what to change.
---

## 3. A matching query mentions the selected item in all tool call outputs

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

     Given a query that matches at least one listing, the suggested_outfit and fit card should both mention at least 1 keyword from the selected_item (specifically, its title) - 4 of 5 tries.


**Why this target:**
     Tool (design/dependencies): The outfit suggestion from outfit_suggestion() and fit card from create_fit_card() rely on model-generated responses, which may result in slightly mismatched phrasings that aren't identical to keywords from the selected_item's title.


---

## 4. A matching query creates a fit card that mentions the price.

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

     Given a query that matches at least one listing, the fit card caption should include the price of the selected item - 4 of 5 tries.

**Why this target:**
     Assuming that search returned at least one listing, the fit card should receive the selected item and outfit description.
     
     Since every listing in data/listings.json has a valid, non-empty price, the fit card caption should include that price. However, it is possible that the price may be missed/not presented properly since create_fit_card() relies on a model-generated response.
     


---

## 5. All queries with a max price select an item below the chosen price.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

     If a max price is included in the query, selected_item must be below the price specified by the user in the query - 4 of 5 tries.

**Why this target:**
     Every listing in data/listings.json has a valid price that can be compared against a specified max price. However, parsing the user's query relies on a model-generated response, and the model may sometimes incorrectly parse or fail to recognize a max price.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
