# বাংলা কিবোর্ড (Bangla Keyboard)

Avro-স্টাইল বাংলা কিবোর্ড — Keyman দিয়ে তৈরি, **ক্রস-প্ল্যাটফর্ম** (Windows / macOS / Linux / Android / iOS)।
অ্যান্টিভাইরাস ফলস-পজিটিভ সমস্যা নেই, কারণ Keyman ইঞ্জিন নিজেই সাইনড ও বিশ্বস্ত।

দুটি লেআউট:

| লেআউট | ফোল্ডার | বর্ণনা |
|-------|---------|--------|
| **ফোনেটিক** (অভ্র-স্টাইল) | `bangla_phonetic/` | ইংরেজি বানানে টাইপ → বাংলা। অটো-যুক্তাক্ষর, কার, স্পেশাল যুক্তাক্ষর (ক্ষ, জ্ঞ, ঋ/ৃ), বাংলা সংখ্যা। |
| **প্রভাত** (ফিক্সড) | `bangla_fixed/` | ফিক্সড লেআউট, m17n-db থেকে অথেনটিক ম্যাপিং। |

## বিল্ড

দরকার: [Keyman Developer](https://keyman.com/developer/) অথবা CLI কম্পাইলার:

```bash
npm install -g @keymanapp/kmc
cd bangla_phonetic && kmc build      # -> build/bangla_phonetic.kmp
cd ../bangla_fixed && kmc build      # -> build/bangla_fixed.kmp
```

অথবা একসাথে: `./build-all.sh`

## ইনস্টল

- **Windows / macOS / Linux:** [Keyman](https://keyman.com/) বসিয়ে `.kmp` ফাইলে ডাবল-ক্লিক।
- **Android / iOS:** Keyman অ্যাপে `.kmp` খুলুন।
- **ওয়েব টেস্ট:** প্রতিটি `build/*.js` ফাইল [KeymanWeb](https://keyman.com/developer/keymanweb)-এ।

## ফোনেটিক স্কিম (সংক্ষেপে)

- স্বর: `a`→আ/া, `i`→ই/ি, `u`→উ/ু, `e`→এ/ে, `O`→ও/ো; `o` = অন্তর্নিহিত স্বর (যুক্তাক্ষর ভাঙে)
- ব্যঞ্জন: `k`→ক, `kh`→খ, `g`→গ, `T`→ট, `t`→ত … (পূর্ণ তালিকা টাইপিং গাইডে)
- যুক্তাক্ষর: পরপর দুই ব্যঞ্জন → যুক্ত; যেমন `kt`→ক্ত, `projukti`→প্রযুক্তি
- স্পেশাল: `x`→ক্ষ, `gg`→জ্ঞ, `rri`→ঋ, `(ব্যঞ্জন)rri`→ৃ-কার
- সংখ্যা: `0-9`→০-৯

সোর্স জেনারেটর: `_build/` (Python স্ক্রিপ্ট দিয়ে `.kmn` রুল তৈরি হয়)।

## লাইসেন্স
MIT (প্রতিটি কিবোর্ড ফোল্ডারে `LICENSE.md` দেখুন)।
