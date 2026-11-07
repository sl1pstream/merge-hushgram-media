# merge-hushgram-media

This is a script that works alongside [Morphe Manager](https://github.com/MorpheApp/morphe-manager) and [HushGram](https://github.com/SysAdminDoc/HushGram) patches for Instagram on Android. If that sentence means nothing to you, just pretend like you didn't see this

### Why this exists
Currently, HushGram's media saving saves pictures and videos into **2 separate directories**. This causes a slight redundancy of 2 albums visible in your galery app (or the bigger redundancy of 2 of each username when `Folder per acocunt` is enabled in HushGram settings). This reconciles that by moving them all to Download/HushGram, keeping subfolders if necessary

### How the scripts work
**Please note that this only works if you haven't changed `Save folder`. If you changed this, you will need to modify the script to use the right directories**
I made 2 versions of this script: one that works with `Folder per account` enabled, and one that works regardless.

Both scripts check the following directories:
Pictures/Instagram
Movies/Instagram

**Script for `Folder per account`** takes all subfolders in both directories and moves them to Download/HushGram. If a folder with the same name exists, it merges the contents. Duplicate files are renamed, and the original subfolder and its files are deleted after the movee.
**Script without `Folder per account`** just moves everything in the 2 directories into Download/HushGram and renames duplicate files

## How to use this
I'd recommend using this alongside [MacroDroid](https://play.google.com/store/apps/details?id=com.arlosoft.macrodroid&hl=en) and [Termux](https://github.com/termux/termux-app):

**Triggers:** Application Closed - Instagram (It doesn'*have* to be that, but I did find that the most efficient without relying on an time interval based check, since most everyday saves are done by the time you close out of the app anyway)

You will need to create a wrapper for your script. In Termux:
1. `mkdir -p /.termux/tasker`
2. Creating the wrapper:
   ```
   cat > ~/.termux/tasker/merge_hushgram <<'EOF' #!/data/data/com.termux/files/usr/bin/bash
   python "path/to/the/downloaded/script"
   EOF
   ```
3. Make it executable: `chmod +x ~/.termux/tasker/merge_hushgram`
4. Test it (just in case): `~/.termux/tasker/merge_hushgram`

**Actions:** Applications - Tasker/Locale Plugin - Termux:Tasker - Termux
- In the Executable field, type `merge_hushgram`, then save (floppy disk icon at the top right)
- If you see a Variables screen, just hit OK.

It should look something like this if you've done it right:

<img width="182" height="400" alt="Screenshot_2026-11-07-00-05-05-44_2e840d222d67ef3caca3a1c67d71d48f" src="https://github.com/user-attachments/assets/3c8db471-1704-464d-a97f-18ae287821ef" />

---
**Note about AI-generated code:** I have minimal experience with python, enough to be able to read and understand what the script itself does. The problem is, I make too many typos and spend hours rewriting the simplest of scripts because I struggle with planning. I use downloaded LLMs to generate code so I won't lose time because of the shortcoming. I don't like using cloud-based models since they contribute a lot to the overuse of electricity and natural resources.
