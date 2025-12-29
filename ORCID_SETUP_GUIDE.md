# ORCID Registration Guide - Quick Setup

**Time Required:** 5-10 minutes
**Cost:** Free
**Required:** Yes (for DIB submission)

---

## What is ORCID?

**ORCID (Open Researcher and Contributor ID)** is a unique identifier for researchers, like a DOI for people. It helps:
- Distinguish you from other researchers with similar names
- Link all your publications together
- Make your work more discoverable
- Required by most journals (including Data in Brief)

**Your ORCID:** A permanent 16-digit number like `0000-0002-1234-5678`

---

## Step 1: Check if You Already Have an ORCID

### Visit: https://orcid.org

**Try to sign in with:**
- Your institutional email: jj.cruza@up.edu.pe
- Or any other email you've used for research

**If you can sign in:** ✅ You already have an ORCID! Skip to Step 3.

**If you can't sign in:** ⏭️ Continue to Step 2.

---

## Step 2: Register for ORCID (New Account)

### Go to: https://orcid.org/register

### Fill in the form:

**Required Information:**
- **First name:** Jason
- **Last name:** Cruz
- **Email:** jj.cruza@up.edu.pe *(use institutional email)*
- **Password:** *(create a strong password)*
- **Confirm password:** *(same as above)*

**Optional (but recommended):**
- **Also known as:** Jason J. Cruz, J. Cruz, etc.
- **Country:** Peru
- **Primary institution:** Universidad del Pacífico

**Privacy Settings:**
- **Who can see your email?** → Select "Everyone" or "Trusted parties"
  *(Journals need to verify)*
- **Who can see your ORCID?** → Select "Everyone"
  *(Make your work discoverable)*

### Click "Register"

### Verify your email:
1. Check your inbox: jj.cruza@up.edu.pe
2. Open email from ORCID
3. Click verification link
4. **Done!** ✅

---

## Step 3: Get Your ORCID Number

### After logging in:

1. Your ORCID appears at the top of your profile page
2. Format: `https://orcid.org/0000-0002-XXXX-XXXX`
3. **Copy the full URL** or just the **16-digit number**

**Example:**
```
Full URL:  https://orcid.org/0000-0002-1825-0097
Just ID:   0000-0002-1825-0097
```

**📋 COPY YOUR ORCID HERE:**
```
ORCID: _______________________________
```

---

## Step 4: Add Information to Your ORCID Profile (Optional but Recommended)

### Education:
1. Click "Add education"
2. Institution: Universidad del Pacífico
3. Degree: *(your degree)*
4. Dates: *(start - end or "present")*

### Employment:
1. Click "Add employment"
2. Organization: Universidad del Pacífico - CIUP
3. Role: *(your position)*
4. Dates: *(start - present)*

### Works (Add after publication):
1. Click "Add works"
2. Search by DOI or add manually
3. Your DIB paper will automatically link after publication

---

## Step 5: Update CITATION.cff

After getting your ORCID, update the file:

**Current (CITATION.cff line 12):**
```yaml
orcid: "https://orcid.org/0000-0000-0000-0000"  # TODO: Add your ORCID
```

**Replace with your real ORCID:**
```yaml
orcid: "https://orcid.org/0000-0002-XXXX-XXXX"  # Your actual ORCID
```

**Command to update:**
```bash
# Open CITATION.cff in your editor
# Replace line 12 with your ORCID
# Save the file
# Then commit:
git add CITATION.cff
git commit -m "docs: add ORCID to CITATION.cff"
git push
```

---

## Step 6: Add ORCID to Other Files

### Files that need your ORCID:

1. **DIB_MANUSCRIPT_DRAFT.md** (line ~41)
   - Replace: `[YOUR_ORCID_ID]`
   - With: `0000-0002-XXXX-XXXX`

2. **ZENODO_README.md** (line ~236)
   - Replace: `[Your ORCID ID]`
   - With: `0000-0002-XXXX-XXXX`

3. **When submitting to Zenodo:**
   - Use "Sign in with ORCID" option
   - Auto-links your ORCID to the dataset

4. **When submitting to DIB:**
   - Enter ORCID in author information section
   - Format: `0000-0002-XXXX-XXXX` (without https://)

---

## Common Questions

### Q: Do I need a different ORCID for each paper?
**A:** No! One ORCID for your entire career. All publications link to it.

### Q: Can I change my ORCID later?
**A:** No, ORCID is permanent. But you can update your profile information anytime.

### Q: What if I have publications under different names?
**A:** Add all name variations to your ORCID profile under "Also known as"

### Q: Is ORCID required for DIB?
**A:** Strongly recommended. Makes author identification easier for editors and increases citation tracking.

### Q: What if my institutional email changes?
**A:** You can add multiple emails to your ORCID and set a new primary email.

### Q: Can I use ORCID for non-academic work?
**A:** Yes! ORCID is for all types of research and creative work.

---

## Troubleshooting

### "Email already in use"
- You already have an ORCID! Try "Forgot password?"
- Or try signing in with institutional login

### "Can't verify email"
- Check spam folder
- Make sure you used the correct email
- Resend verification email from ORCID

### "ORCID not showing on profile"
- Make sure privacy is set to "Everyone" can see
- Refresh the page

---

## After Getting ORCID

### ✅ Checklist:

- [ ] ORCID registered and verified
- [ ] ORCID number copied (16 digits)
- [ ] CITATION.cff updated (line 12)
- [ ] DIB_MANUSCRIPT_DRAFT.md updated (search for `[YOUR_ORCID_ID]`)
- [ ] ZENODO_README.md updated (search for `[Your ORCID ID]`)
- [ ] Profile information added (education, employment)
- [ ] Privacy settings set to "Everyone"
- [ ] Changes committed to git

### Next Steps:

After updating ORCID:
1. **Commit changes:** `git add CITATION.cff && git commit -m "docs: add ORCID to CITATION.cff"`
2. **Continue to:** Zenodo upload (when ready)
3. **Use ORCID:** When signing up for Zenodo (auto-links)

---

## Benefits of Having ORCID

✅ **Persistent identifier** - Never changes, even if you change institutions
✅ **Publication tracking** - All your work in one place
✅ **Automatic updates** - Publishers can auto-add publications to your profile
✅ **Disambiguation** - Distinguishes you from others with same name
✅ **Widely adopted** - Recognized by most journals, funders, institutions
✅ **Free forever** - No cost, no ads, non-profit organization

---

## Quick Reference

**Registration:** https://orcid.org/register
**Sign in:** https://orcid.org/signin
**Your profile:** https://orcid.org/0000-0002-XXXX-XXXX *(after registration)*
**Format:** `0000-0002-XXXX-XXXX` (always starts with 0000)
**Support:** support@orcid.org

---

**Estimated Time:** 5-10 minutes
**Status After Completion:** Ready for Zenodo signup (use "Sign in with ORCID")

**Next Document:** ZENODO_UPLOAD_GUIDE.md (Step 1 mentions ORCID option)

---

**Last Updated:** December 28, 2024
**Version:** 1.0
