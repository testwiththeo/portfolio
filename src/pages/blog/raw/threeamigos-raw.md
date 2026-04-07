3️⃣ Three Amigos & BDD — Deep Dive

## 1. Problem Analysis

**🇮🇩** Ini adalah skenario yang terjadi di hampir setiap tim tanpa Three Amigos:

**🇬🇧** This is a scenario that happens in almost every team without Three Amigos:

```
📋 PO writes story  : "User dapat login dengan email dan password"
💻 Dev builds       : Login dengan email + password ✅
🧪 QA tests         : "Tapi bagaimana kalau email tidak terverifikasi?"
😱 Answer           : "Oh... itu belum dihandle sama sekali"
🔥 Result           : Bug di sprint akhir, story tidak bisa di-close
⏰ Cost             : 2 hari extra untuk fix + retest
```

**🇮🇩** Three Amigos + BDD mengeliminasi **ambiguitas** ini **sebelum satu baris kode pun ditulis**.

**🇬🇧** Three Amigos + BDD eliminates this **ambiguity before a single line of code is written**.

---



**🇮🇩** ada yang menyebut Three Amigos sebagai **"Alignment Session"**. Aturannya sederhana: **tidak ada story yang boleh masuk sprint tanpa alignment session ini.** Bukan karena aturan formal — tapi karena tim sudah merasakan sendiri bahwa biaya ambiguitas jauh lebih mahal dari biaya 30 menit meeting.

**🇬🇧** some people called Three Amigos an **"Alignment Session"**. The rule was simple: **no story enters the sprint without this session.** Not because of a formal rule — but because the team had experienced firsthand that the cost of ambiguity is far more expensive than a 30-minute meeting.


---

## 3. Agile Testing Perspective

**🇮🇩** BDD bukan hanya tentang automation — ini tentang **shared language** antara business dan engineering. Gherkin adalah jembatan antara "apa yang PO inginkan" dan "apa yang engineer bangun."

**🇬🇧** BDD is not just about automation — it's about a **shared language** between business and engineering. Gherkin is the bridge between "what the PO wants" and "what engineers build."

```
Without BDD:  PO speaks "business" → Dev speaks "code" → Gap = bugs
With BDD:     Everyone speaks "Given/When/Then" → No gap → Fewer bugs
```

---


---

## 5. Example Implementation

### 📋 Step 1 — Raw Story to Three Amigos Output

**🇮🇩** Mari kita lihat bagaimana sebuah story berubah dari ambigu menjadi presisi melalui Three Amigos session.

**🇬🇧** Let's see how a story transforms from ambiguous to precise through a Three Amigos session.

```
📋 ORIGINAL STORY (Before Three Amigos — Ambiguous):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
As a customer
I want to reset my password
So that I can regain access to my account

Acceptance Criteria:
- User can reset password via email
- Password must be strong

🤔 PROBLEMS QA raises in Three Amigos:
  Q1: What happens if email doesn't exist in system?
  Q2: How long is the reset link valid?
  Q3: What defines "strong" password? (length? symbols?)
  Q4: Can the reset link be used more than once?
  Q5: What happens if user is already logged in?
  Q6: Should old sessions be invalidated after reset?

🔧 DEV raises in Three Amigos:
  D1: Reset tokens stored in DB — need expiry column
  D2: Email service has 500ms latency — need async handling
  D3: Rate limiting needed — prevent abuse

✅ REFINED STORY (After Three Amigos — Precise):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
As a customer
I want to reset my password via a secure email link
So that I can regain access to my account

Acceptance Criteria (Given/When/Then):
  ✅ Valid email receives reset link within 60 seconds
  ✅ Reset link expires after 15 minutes (single-use)
  ✅ New password: min 8 chars, 1 uppercase, 1 special char
  ✅ All existing sessions invalidated after successful reset
  ✅ Non-existent email shows generic message (no enumeration)
  ✅ Max 3 reset requests per hour per email (rate limited)
```

---

### 🥒 Step 2 — Gherkin Scenarios (Full Feature File)

**🇮🇩** Setelah Three Amigos, output langsungnya adalah feature file Gherkin yang komprehensif.

**🇬🇧** After Three Amigos, the direct output is a comprehensive Gherkin feature file.

gherkin

```gherkin
# features/auth/password-reset.feature
# Authors: @po-sarah, @qa-budi, @dev-andi (Three Amigos — Sprint 24)
# Last reviewed: 2025-03-10

Feature: Password Reset via Email
  As a registered customer
  I want to reset my password via a secure email link
  So that I can regain access when I forget my password

  Background:
    Given the system has a registered user with email "budi@example.com"

  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  # HAPPY PATH
  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Scenario: Registered user receives password reset email
    When I request a password reset for "budi@example.com"
    Then a reset email should be sent within 60 seconds
    And the email should contain a secure single-use reset link

  Scenario: User successfully resets password with valid link
    Given a valid password reset link for "budi@example.com"
    When I submit new password "NewSecure@123"
    Then my password should be updated successfully
    And I should see "Password changed successfully"
    And all my existing sessions should be invalidated

  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  # EDGE CASES — raised by QA
  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Scenario: Reset link expires after 15 minutes
    Given a password reset link that was generated 16 minutes ago
    When I attempt to use the expired reset link
    Then I should see "This reset link has expired"
    And I should be prompted to request a new reset link

  Scenario: Reset link cannot be reused after successful reset
    Given I have already used a reset link to change my password
    When I attempt to use the same reset link again
    Then I should see "This reset link has already been used"

  Scenario: Unregistered email shows generic message (prevent enumeration)
    When I request a password reset for "unknown@example.com"
    Then I should see "If this email is registered, you will receive a link"
    And no email should be sent to "unknown@example.com"

  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  # BUSINESS RULES — clarified by PO
  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Scenario: Rate limiting prevents abuse
    Given I have already requested 3 password resets within the last hour
    When I request another password reset for "budi@example.com"
    Then I should see "Too many reset attempts. Please try again in 60 minutes"
    And no email should be sent

  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  # BOUNDARY CONDITIONS — raised by QA + Dev
  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Scenario Outline: Password strength validation
    Given a valid password reset link for "budi@example.com"
    When I submit new password "<password>"
    Then I should see error "<error_message>"

    Examples:
      | password      | error_message                                        |
      | short1!       | Password must be at least 8 characters               |
      | alllowercase1!| Password must contain at least one uppercase letter  |
      | NoSpecial123  | Password must contain at least one special character |
      | NoNumbers!    | Password must contain at least one number            |

  Scenario: Password same as current password is rejected
    Given a valid password reset link for "budi@example.com"
    When I submit the same password as my current one
    Then I should see "New password must be different from your current password"
```

---

### 🔧 Step 3 — Step Definitions (TypeScript + Cucumber + Playwright)

**🇮🇩** Step definitions adalah jembatan antara Gherkin (bahasa bisnis) dan Playwright (kode automation).

**🇬🇧** Step definitions are the bridge between Gherkin (business language) and Playwright (automation code).

typescript

```typescript
// features/auth/password-reset.steps.ts
import { Given, When, Then, Before } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import type { ICustomWorld } from '../support/world';
import { PasswordResetPage } from '../pages/PasswordResetPage';
import { EmailService } from '../support/EmailService';
import { ApiHelper } from '../support/ApiHelper';

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// GIVEN — Setup / Preconditions
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Given('the system has a registered user with email {string}',
  async function (this: ICustomWorld, email: string) {
    // ✅ Use API to seed data — never click through UI for setup
    await ApiHelper.seedUser(this.request, {
      email,
      password: 'OldPassword@123',
      verified: true,
    });
    this.userEmail = email;
  }
);

Given('a valid password reset link for {string}',
  async function (this: ICustomWorld, email: string) {
    // ✅ Generate token via API — no need to simulate email flow
    const { token } = await ApiHelper.generateResetToken(this.request, email);
    this.resetUrl = `/reset-password?token=${token}`;
    await this.page.goto(this.resetUrl);
  }
);

Given('a password reset link that was generated {int} minutes ago',
  async function (this: ICustomWorld, minutesAgo: number) {
    // ✅ Manipulate time via API endpoint — no real waiting
    const { token } = await ApiHelper.generateResetToken(
      this.request,
      this.userEmail,
      { createdMinutesAgo: minutesAgo }
    );
    this.resetUrl = `/reset-password?token=${token}`;
    await this.page.goto(this.resetUrl);
  }
);

Given('I have already requested {int} password resets within the last hour',
  async function (this: ICustomWorld, count: number) {
    for (let i = 0; i < count; i++) {
      await ApiHelper.generateResetToken(this.request, this.userEmail);
    }
  }
);

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// WHEN — Actions
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When('I request a password reset for {string}',
  async function (this: ICustomWorld, email: string) {
    const resetPage = new PasswordResetPage(this.page);
    await resetPage.goto();
    await resetPage.requestReset(email);
    this.submittedEmail = email;
  }
);

When('I submit new password {string}',
  async function (this: ICustomWorld, password: string) {
    const resetPage = new PasswordResetPage(this.page);
    await resetPage.submitNewPassword(password);
  }
);

When('I submit the same password as my current one',
  async function (this: ICustomWorld) {
    const resetPage = new PasswordResetPage(this.page);
    await resetPage.submitNewPassword('OldPassword@123'); // matches seeded password
  }
);

When('I attempt to use the expired reset link',
  async function (this: ICustomWorld) {
    await this.page.goto(this.resetUrl);
  }
);

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// THEN — Assertions
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Then('a reset email should be sent within {int} seconds',
  async function (this: ICustomWorld, seconds: number) {
    // ✅ Poll email inbox via API — no fragile time.sleep()
    const email = await EmailService.waitForEmail(
      this.submittedEmail,
      { subject: 'Reset your password', timeoutMs: seconds * 1000 }
    );
    expect(email).toBeTruthy();
    this.resetEmail = email;
  }
);

Then('I should see {string}',
  async function (this: ICustomWorld, message: string) {
    await expect(
      this.page.locator('[data-testid="feedback-message"]')
    ).toContainText(message);
  }
);

Then('all my existing sessions should be invalidated',
  async function (this: ICustomWorld) {
    // ✅ Verify via API — check session store directly
    const sessions = await ApiHelper.getActiveSessions(
      this.request,
      this.userEmail
    );
    expect(sessions).toHaveLength(0);
  }
);

Then('no email should be sent to {string}',
  async function (this: ICustomWorld, email: string) {
    // ✅ Wait briefly then assert no email arrived
    const received = await EmailService.checkNoEmailReceived(email, {
      waitMs: 3000
    });
    expect(received).toBe(false);
  }
);
```

---

### 🏗️ Step 4 — Page Object Model (TypeScript + Playwright)

**🇮🇩** Page Object Model memisahkan **logika UI** dari **logika test** — membuat step definitions bersih dan reusable.

**🇬🇧** The Page Object Model separates **UI logic** from **test logic** — keeping step definitions clean and reusable.

typescript

```typescript
// features/pages/PasswordResetPage.ts
import type { Page } from '@playwright/test';

export class PasswordResetPage {
  private readonly selectors = {
    emailInput:       '[data-testid="reset-email-input"]',
    submitBtn:        '[data-testid="reset-submit-btn"]',
    newPasswordInput: '[data-testid="new-password-input"]',
    confirmPwdInput:  '[data-testid="confirm-password-input"]',
    changePasswordBtn:'[data-testid="change-password-btn"]',
    feedbackMessage:  '[data-testid="feedback-message"]',
    errorMessage:     '[data-testid="error-message"]',
  } as const;

  constructor(private readonly page: Page) {}

  async goto(): Promise<void> {
    await this.page.goto('/forgot-password');
    await this.page.waitForSelector(this.selectors.emailInput);
  }

  async requestReset(email: string): Promise<void> {
    await this.page.fill(this.selectors.emailInput, email);
    await this.page.click(this.selectors.submitBtn);
    // ✅ Wait for server response, not arbitrary time
    await this.page.waitForResponse(
      (res) => res.url().includes('/api/auth/reset-request')
    );
  }

  async submitNewPassword(password: string): Promise<void> {
    await this.page.fill(this.selectors.newPasswordInput, password);
    await this.page.fill(this.selectors.confirmPwdInput, password);
    await this.page.click(this.selectors.changePasswordBtn);
    await this.page.waitForResponse(
      (res) => res.url().includes('/api/auth/reset-password')
    );
  }

  async getErrorMessage(): Promise<string> {
    return this.page.locator(this.selectors.errorMessage).innerText();
  }
}
```

---

### 🌍 Step 5 — World Object (Shared State Between Steps)

**🇮🇩** World object menyimpan shared state antar step dalam satu scenario — seperti `userEmail`, `resetUrl`, dll.

**🇬🇧** The World object holds shared state between steps in one scenario — like `userEmail`, `resetUrl`, etc.

typescript

```typescript
// features/support/world.ts
import { World, setWorldConstructor } from '@cucumber/cucumber';
import { Browser, BrowserContext, Page, APIRequestContext } from '@playwright/test';
import { chromium } from 'playwright';

export interface ICustomWorld extends World {
  browser: Browser;
  context: BrowserContext;
  page: Page;
  request: APIRequestContext;
  // Shared state — set in Given, read in Then
  userEmail: string;
  resetUrl: string;
  resetEmail: Record<string, string> | null;
  submittedEmail: string;
}

class CustomWorld extends World implements ICustomWorld {
  browser!: Browser;
  context!: BrowserContext;
  page!: Page;
  request!: APIRequestContext;
  userEmail = '';
  resetUrl = '';
  resetEmail = null;
  submittedEmail = '';
}

setWorldConstructor(CustomWorld);

// features/support/hooks.ts
import { Before, After } from '@cucumber/cucumber';
import { chromium, request as playwrightRequest } from 'playwright';
import type { ICustomWorld } from './world';

Before(async function (this: ICustomWorld) {
  this.browser = await chromium.launch();
  this.context  = await this.browser.newContext();
  this.page     = await this.context.newPage();
  this.request  = await playwrightRequest.newContext({
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
  });
});

After(async function (this: ICustomWorld, scenario) {
  // ✅ Capture screenshot on failure — self-documenting CI artifacts
  if (scenario.result?.status === 'FAILED') {
    const screenshot = await this.page.screenshot({ fullPage: true });
    this.attach(screenshot, 'image/png');
  }
  await this.page.close();
  await this.context.close();
  await this.browser.close();
  await this.request.dispose();

  // ✅ Always clean up test data — don't pollute shared environments
  await ApiHelper.cleanupUser(this.userEmail);
});
```

---

### 📊 Step 6 — Living Documentation Report

**🇮🇩** Salah satu keunggulan BDD adalah **living documentation** — laporan yang bisa dibaca oleh semua stakeholder, bukan hanya engineer.

**🇬🇧** One of BDD's greatest advantages is **living documentation** — reports readable by all stakeholders, not just engineers.

jsonc

```jsonc
// cucumber.json — report config
{
  "default": {
    "paths": ["features/**/*.feature"],
    "require": ["features/**/*.steps.ts", "features/support/*.ts"],
    "requireModule": ["ts-node/register"],
    "format": [
      "progress-bar",
      "html:reports/cucumber-report.html",   // Human-readable HTML
      "json:reports/cucumber-report.json"    // For CI integration
    ],
    "formatOptions": { "snippetInterface": "async-await" }
  }
}
```

```
📊 SAMPLE LIVING DOCUMENTATION OUTPUT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Feature: Password Reset via Email
  ✅ Registered user receives password reset email         (1.2s)
  ✅ User successfully resets password with valid link     (2.1s)
  ✅ Reset link expires after 15 minutes                   (0.8s)
  ✅ Reset link cannot be reused after successful reset    (0.9s)
  ✅ Unregistered email shows generic message              (0.7s)
  ✅ Rate limiting prevents abuse                          (1.0s)
  ✅ Password same as current is rejected                  (0.8s)
  ✅ Scenario Outline: Password strength (4 examples)      (3.2s)

  12 scenarios (12 passed)
  48 steps (48 passed)
  Duration: 10.7s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ Business stakeholders can read this — no engineering jargon!
```

---

## 6. Common Mistakes

**🇮🇩** Kesalahan yang paling sering terjadi saat tim mengadopsi Three Amigos & BDD:

**🇬🇧** The most common mistakes when teams adopt Three Amigos & BDD:

gherkin

```gherkin
# ❌ MISTAKE 1: Gherkin yang terlalu teknis — ini bukan BDD
Scenario: API returns 200 with correct JSON schema
  Given POST /api/auth/reset with body {"email": "test@test.com"}
  When response status is 200
  Then JSON body contains "token" field of type string

# ✅ RIGHT: Business language — PO bisa baca dan validasi
Scenario: Registered user receives password reset email
  Given I am a registered user with email "budi@example.com"
  When I request a password reset
  Then I should receive a password reset email within 60 seconds


# ❌ MISTAKE 2: UI steps di setiap scenario (slow & brittle)
Given I open the browser
And I navigate to "https://app.example.com/login"
And I click the login button
And I type "budi@example.com" in the email field
And I type "Password123!" in the password field
And I click the submit button
And I wait for the dashboard to load
# → This is a UI script, not a behavior scenario

# ✅ RIGHT: Use Background + API setup for preconditions
Background:
  Given I am logged in as a registered customer
# Implemented via API call — no UI clicks needed


# ❌ MISTAKE 3: One mega-scenario testing everything
Scenario: Full password reset flow
  Given I am on the login page
  When I click forgot password
  And I enter my email
  And I receive an email
  And I click the link
  And I enter a new password
  And I confirm the password
  And I submit
  Then I should be logged in
  And my old password should not work
  And I should see a success toast
  And my sessions should be cleared
  And an audit log should be created
# → Too many assertions — hard to debug when it fails

# ✅ RIGHT: One scenario, one behavior
Scenario: Successful reset invalidates all existing sessions
  Given I have 3 active sessions on different devices
  And a valid password reset link for "budi@example.com"
  When I submit new password "NewSecure@456"
  Then all 3 existing sessions should be invalidated
```

---

## 7. Pro Tips
**💎 Tip 1 — "Example Mapping" Before Writing Gherkin**
**🇮🇩** sebelum menulis Gherkin, kami menggunakan teknik **Example Mapping** menggunakan sticky notes (atau Miro). Ini membantu visualisasi semua scenario dalam 10 menit.

**🇬🇧**before writing Gherkin, we used **Example Mapping** with sticky notes (or Miro). It helps visualize all scenarios in 10 minutes.

```
Example Mapping Structure (color-coded cards):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟡 STORY (yellow)     : "Password Reset"
🔵 RULES (blue)       : "Link expires in 15 min"
                         "Max 3 requests/hour"
                         "New pwd ≠ old pwd"
🟢 EXAMPLES (green)   : "Valid link → success"
                         "Expired link → error message"
                         "4th request → rate limited"
🔴 QUESTIONS (red)    : "Do we notify on successful reset?"
                         "What about OAuth users — no password?"
                         "Mobile app deep link or web URL?"

Red cards = questions that BLOCK the story from being Ready
All red cards must be answered before development starts
```

---


**🇮🇩** Gherkin yang baik mendeskripsikan **WHAT** terjadi, bukan **HOW** melakukannya. Semakin deklaratif, semakin stabil terhadap perubahan UI.

**🇬🇧** Good Gherkin describes **WHAT** happens, not **HOW** to do it. The more declarative, the more resilient to UI changes.



```gherkin
# ❌ IMPERATIVE (describes HOW — fragile, breaks on UI change)
When I click the button with id "submit-reset-form"
And I wait 2 seconds
And I check the div class "alert-success" contains "Password changed"

# ✅ DECLARATIVE (describes WHAT — stable, UI-change resilient)
When I submit my new password
Then I should see a password change confirmation
```

---

BDD is a Conversation Tool, Not Just a Test Tool**

**🇮🇩** Kesalahan paling fatal: tim menggunakan BDD hanya untuk automation, tanpa Three Amigos session yang sesungguhnya. Hasilnya adalah Gherkin yang ditulis oleh QA sendiri setelah development selesai — ini bukan BDD, ini hanya **test scripting dengan syntax Gherkin.**

**🇬🇧** The most fatal mistake: teams use BDD only for automation, without real Three Amigos sessions. The result is Gherkin written by QA alone after development is complete — this isn't BDD, it's just **test scripting with Gherkin syntax.**

```
❌ FAKE BDD:  Dev builds → QA writes Gherkin → QA automates
              (Just test scripting — no alignment benefit)

✅ REAL BDD:  Three Amigos → Gherkin agreed → Dev builds
              → QA automates → Living docs always up-to-date
              (True alignment — bugs prevented, not just found)
```

---

## 🎯 Quick Summary

```
✅ Three Amigos  → Dev + QA + PO. 30 min. Before every sprint story.
✅ Output        → Gherkin scenarios, agreed by all 3 roles.
✅ Gherkin rules → Declarative not imperative. Business language.
✅ Step defs     → Bridge Gherkin to Playwright. Use Page Objects.
✅ World object  → Shared state across steps. Clean up in After hook.
✅ Living docs   → HTML report stakeholders can read and validate.
✅ Example Map   → Use before writing Gherkin. Red cards = blockers.
✅ Never         → Write Gherkin after development. That's not BDD.
```

---
