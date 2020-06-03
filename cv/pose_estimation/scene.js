        var canvas = document.getElementById("renderCanvas");

        var engine = null;
        var scene = null;
        var sceneToRender = null;
        var createDefaultEngine = function() {
            return new BABYLON.Engine(
                canvas, true, { preserveDrawingBuffer: true, stencil: true }
            );
        };

        var createScene = function () {
            sceneFile = "_scene.babylon" // <-- !! Change to the right sceneFile
            bgImageName = "IMG_5912_image.jpg" // <-- !! Change to the right image

            var s3BaseUrl = "https://arinthewild.s3.amazonaws.com/quick_design_images/"
            var scene = new BABYLON.Scene(engine);
            BABYLON.SceneLoader.Append(s3BaseUrl, sceneFile, scene, function (){
                scene.activeCamera = scene.cameras[1];
            });

            var camera = new BABYLON.UniversalCamera("UniversalCamera", new BABYLON.Vector3(0 ,0, 0), scene);

            /* Insert background image */
            var bgImageUrl = s3BaseUrl + bgImageName
            var bg = new BABYLON.Layer("bgImage", bgImageUrl, scene);
            bg.isBackground = true;
            bg.texture.level = 0.0;
            bg.texture.wAng = 0.0;
            scene.activeCamera.detachControl(canvas);
            return scene;
        };

        engine = new BABYLON.Engine(canvas, true);
        if (!engine) throw 'engine should not be null.';
        scene = createScene();
        sceneToRender = scene;

        engine.runRenderLoop(function () {
            if (sceneToRender) {
                sceneToRender.render();
            }
        });
