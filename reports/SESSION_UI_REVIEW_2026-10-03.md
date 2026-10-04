# U09 — Compact Session delivery

S01 0.8 · U09 · R25/R26 · T32–T34. Original public UI code; no private Nucleus artifacts used.

## Observed
- Desktop: renamed Session, removed visible message label and upper agent toolbar, added provider/model/effort/agent dropdowns below the text, compact connection status and decorative rotating invitation.
- Browser fixture: Anthropic selection showed Sonnet, Opus, Fable and Haiku. Haiku disabled effort at Standard. Opus high reached the simulated transport as high. Changing to low retained three conversation messages in the next call. Changing to Sonnet cleared messages and preserved a typed draft.
- Provider switch disconnected the old session; it did not reuse its key. ES/EN preserved draft and selections. Connect and send are distinct states of the composer arrow.
- Narrow viewport 390 x 844: document scrollWidth equaled clientWidth (375 CSS pixels after scrollbar); dropdowns wrapped into two columns. Enter expanded the sidebar; selecting Agents collapsed it again. Temporary viewport override was reset.
- Automated: seven new tests cover real wire payload shape, unsupported combinations, atomic model changes and history/budget preservation, busy guard, disconnect during configuration and reference-catalog copies. Full validation reports 90 tests plus seven scenarios; see evidence/latest.json for final result.

## Limits
Model responses in browser checks came from local doubles. No real OpenAI or Anthropic request was made. Catalog entries describe supported choices, not live account entitlement. Qualitative speed hints are based on provider documentation; this application has no measured latency guarantee or premium speed tier. Reduced-motion handling and animation pause are implemented in source; no assistive-technology certification or exhaustive accessibility audit is claimed. Higher effort may exhaust the explicit output/time limit. Other-PC execution, owner acceptance and independent review remain separate.

See [connection guide and sources](../docs/OPENAI_API.md). The new screenshot shows the real local UI with no credentials or mocked model response.
