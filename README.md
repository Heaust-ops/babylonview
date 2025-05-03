# Babylon View

A blender addon that lets you view your [babylonjs](https://www.babylonjs.com/) scenes in [blender](https://www.blender.org/).

I'd love for you to try this out and give me your thoughts :)

Babylonjs discussion thread: [https://forum.babylonjs.com/t/a-blender-addon-for-babylonjs-scene-viewing/57580](https://forum.babylonjs.com/t/a-blender-addon-for-babylonjs-scene-viewing/57580).

- [How to install](#how-to-install)
- [How to use](#how-to-use)
- [Workflows / How it looks](#workflows)
- [Bug Reporting](#bug-reporting)

## How to install

### Step 1: Download this repo as zip.

You can do this by clicking on the green `Code` button on this page, and then clicking on `Download Zip`

![How to download repo as zip](https://github.com/user-attachments/assets/2fd91994-039f-4aab-9600-6c309bc3a49f)

### Step 2: Install the zip as an addon.

To install an addon, open up blender and go to: Edit > Preferences > Add-ons > Install

![How to install a blender addon](https://github.com/user-attachments/assets/198a1f57-980a-40e5-a920-8b39b0e1bbef)

Now go to your `Downloads` folder, select the file named `"babylonview-main.zip"` and click on `Install Add-on`

![Select the downloaded addon to install](https://github.com/user-attachments/assets/6cf030f1-edf2-4be1-a68c-213eb63ec248)

### Step 3: Enabling the addon.

That's is the addon is installed!

Now to enable it, search for "babylonjs view" in your addons, click on the checkbox and you're done!

![Enabling the installed addon](https://github.com/user-attachments/assets/d98e2cee-00c4-4973-a1cd-f32e235fd1a7)

and that's it! you have the addon integrated :)

## How to use

### Step 1: Open your views sidebar.

Hit the `"n"` key on your keyboard to open the views sidebar, you'll see a new `"Babylon.js View"` tab on it, click on it.

![Babylon.js View sidebar in the views sidebar](https://github.com/user-attachments/assets/e81dddc6-e8e7-4c13-94ee-523effab71a2)

### Step 2: Start the server.

Once you're in the `"Babylon.js View"` tab, you should see a button that says `"Start Server"`, click on it.

![How to start the server](https://github.com/user-attachments/assets/9fe9659f-d582-4699-be78-98fef1f54a74)

Congrats! you have the addon turned on now :)

![Notification that the server has started](https://github.com/user-attachments/assets/0c55a8a9-daf0-46a0-a2fd-6ee07f656140)

### Step 3: Open up the babylonjs view in your browser.

Open up your browser _(Google Chrome, Mozilla Firefox, Edge... etc)_ and type `localhost:8001` in your url bar and hit the `Enter` key

![babylon view opened up in a browser](https://github.com/user-attachments/assets/499658c5-91e3-432c-b1ad-aefa477f692f)

It may take a while if your scene is large, please be patient, but your blender scene should now load up in your browser using babylonjs!

You'll also see 3 buttons at the bottom.

Use the `"glb sync"` button to sync your babylonjs scene whenever you make changes in blender so they reflect in your browser.

This is quite slow as it does a full gltf export/import.

If you want something faster and more realtime, click on the `"realtime sync"` button and that'll turn on the `realtime sync` mode, any changes you do in blender will be instantly reflected in your browser.

The `"babylonjs inspector"` button opens up the `Babylonjs Inspector` for you to inspect your scene.

## Workflows

### Glb Sync

If you're just occasionally glancing at your browser window, it might be a good idea to use the `"glb sync"` button to update the scene whenever you occasionally need to.

This because the Glb Sync mode is more stable and gaurantees (as of right now) complete translation of your scene, whereas the realtime mode might introduce inconsistencies over time, and waste precious resources computing.

Here's how one might use this workflow.

https://github.com/user-attachments/assets/ded9561a-a1fb-4768-be91-5aedf99c1d12

### Realtime Sync

If the model you're working with is large, glb sync may take a lot of time. or you might want to more actively monitor your changes, for example when focusing on getting things right in babylonjs.

here's how you might use the Realtime workflow.

https://github.com/user-attachments/assets/94ed0990-558f-4673-9f8c-507d63171408

### Mustang Showcase

Here's how this [free mustang scene](https://www.blenderkit.com/get-blenderkit/451fc6ed-c9f5-499d-aa3d-fd5a41b02614/) from [blenderkit](https://www.blenderkit.com/) looks :)

https://github.com/user-attachments/assets/4713afd9-db88-496a-9d61-6851f4344ee1

## Bug Reporting

If you face any issues with this addon, feel free to post it on the issues section of this repository.

It would help if you included these details in your issue report,

- what you issue is!
- what you were expecting.
- how you encountered the issue.
- steps to reliably reproduce the issue.

and that's kind of it!

If you'd like addon to do extra stuff, have more features, please submit your feature request as an issue too!

In that case please provide these details,

- What feature do you want!
- Why you want it.
- How much of an impact this would make for you and your experience.

That's it.

---

Have fun!
