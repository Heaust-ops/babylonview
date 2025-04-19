# Babylon View

A blender addon that lets you view your babylonjs scenes in blender, currently in active dev.

But I'd love for you to try this out and give me your thoughts :)

Babylonjs discussion thread: [https://forum.babylonjs.com/t/a-blender-addon-for-babylonjs-scene-viewing/57580](https://forum.babylonjs.com/t/a-blender-addon-for-babylonjs-scene-viewing/57580).

- [How to install](#how-to-install)
- [How to use](#how-to-use)

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

If you want something faster and more realtime, click on the `"realtime sync"` button and that'll turn on the `realtime sync` mode, any changes you do in blender will be instantly reflected in your browser. Please note this feature is still in active dev and does not gaurantee a perfect experience as of yet.

The `"babylonjs inspector"` button opens up the `Babylonjs Inspector` for you to inspect your scene.

Have fun!
