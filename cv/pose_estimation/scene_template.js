        var canvas = document.getElementById("renderCanvas");

        var engine = null;
        var scene = null;
        var sceneToRender = null;
        var createDefaultEngine = function() { return new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true }); };

        //This comes from layout + scene.build()
        var config = {{SCENE_INFO}};

        var createScene = function () {
            var scene = new BABYLON.Scene(engine);
            var camera = new BABYLON.UniversalCamera("UniversalCamera", new BABYLON.Vector3(0 ,0, 0), scene);
            camera.name = "camera.001";
            camRotation = config.camera.rotation
            rx = camRotation[0]
            ry = camRotation[1]
            rz = camRotation[2]
            scene.activeCamera.rotation = new BABYLON.Vector3(rx, ry, rz);
            camPosition = config.camera.position
            var r = 1.0;
            cx = r * camPosition[0]
            cy = r * camPosition[1]
            cz = r * camPosition[2]
            scene.activeCamera.position = new BABYLON.Vector3(cx, cy, cz);
            scene.activeCamera.fov = config.camera.fov;

            // the GLB model to be inserted into the scene.

            /* Insert background image */
            var bgImageUrl = "{{BACKGROUND_IMAGE}}";
            var bg = new BABYLON.Layer("bgImage", bgImageUrl, scene);
            bg.isBackground = true;
            bg.texture.level = 0.0;
            bg.texture.wAng = 0.0;

            var plane = config.walls.FLOOR;
            var origin = plane.position;
            var rotation = plane.rotation

            // Ground
            var groundMaterial = new BABYLON.StandardMaterial("groundMaterial", scene);
            groundMaterial.specularColor = BABYLON.Color3.Black();
            groundMaterial.alpha = 1.0;
            size = 2.
            var ground = BABYLON.MeshBuilder.CreateGround("ground", {width:size[0], height:size[1]}, scene, false);
            ground.rotation = new BABYLON.Vector3(rotation[0], rotation[1], rotation[2]);
            ground.position.x = origin[0];
            ground.position.y = origin[1];
            ground.position.z = origin[2];
            ground.material = groundMaterial;

            var sphere = BABYLON.MeshBuilder.CreateSphere("sphere", {diameter: 1}, scene);
            sphere.position.x = origin[0];
            sphere.position.y = origin[1];
            sphere.position.z = origin[2];


            //var light = new BABYLON.PointLight("pointLight", new BABYLON.Vector3(origin[0], 10 * origin[1], 5 * origin[2]), scene);
            //var light = new BABYLON.HemisphericLight("HemiLight", new BABYLON.Vector3(0, 1, 0), scene);

            var light = new BABYLON.DirectionalLight("DirectionalLight", new BABYLON.Vector3(0, -1, 0), scene);
            light.intensity = 5.;

            var light1 = new BABYLON.DirectionalLight("DirectionalLight", new BABYLON.Vector3(0, 1, 0), scene);
            light1.intensity = 5.;

            scene.activeCamera.detachControl(canvas);

            // var totalMesh = sphere;

            // Interaction
            var startingPoint;
            var currentMesh;
            let ROTATE_Z = new BABYLON.Vector3(0, 1, 0);

            var getGroundPosition = function () {
                var pickinfo = scene.pick(scene.pointerX, scene.pointerY, function (mesh) { return mesh == ground; });
                if (pickinfo.hit) {
                    return pickinfo.pickedPoint;
                }
                return null;
            }

            var pointerDown = function (mesh) {
                    currentMesh = mesh;
                    startingPoint = getGroundPosition();
                    if (startingPoint) { // we need to disconnect camera from canvas
                        setTimeout(function () {
                            scene.activeCameras.detachControl(canvas);
                        }, 0);
                    }
            }

            var keyDown = function (mesh) {
                    currentMesh = mesh;
                    startingPoint = getGroundPosition();
                    if (startingPoint) { // we need to disconnect camera from canvas
                        setTimeout(function () {
                            scene.activeCameras.detachControl(canvas);
                        }, 0);
                    }
            }


            var pointerUp = function () {
                if (startingPoint) {
                    //camera.attachControl(canvas, true);
                    startingPoint = null;
                    return;
                }
            }

            var pointerMove = function () {
                if (!startingPoint) {
                    return;
                }
                var current = getGroundPosition();
                if (!current) {
                    return;
                }

                var diff = current.subtract(startingPoint);
                //diff = diff.multiplyByFloats(.3, .3, .3);
                currentMesh.position.addInPlace(diff);

                startingPoint = current;

            }

            scene.onPointerObservable.add((pointerInfo) => {
                switch (pointerInfo.type) {
                    case BABYLON.PointerEventTypes.POINTERDOWN:
                        if(pointerInfo.pickInfo.hit && pointerInfo.pickInfo.pickedMesh != ground) {
                            pointerDown(pointerInfo.pickInfo.pickedMesh)
                        }
                        break;
                    case BABYLON.PointerEventTypes.POINTERUP:
                            pointerUp();
                        break;
                    case BABYLON.PointerEventTypes.POINTERMOVE:
                            pointerMove();
                        break;
                }
            });



            var unitVec = new BABYLON.Vector3(0, 1, 0);

            var advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI", true, scene);

            var slider = new BABYLON.GUI.Slider();
            slider.minimum = 0.0;
            slider.maximum = 2 * 3.141592;
            slider.value = 0;
            slider.height = "20px";
            slider.width = "150px";
            slider.color = "#003399";
            slider.background = "grey";
            slider.left = "120px";
            slider.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
            slider.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_CENTER;
            slider.onValueChangedObservable.add(function (value) {
                totalMesh.rotation = unitVec.scale(value);
            });

            advancedTexture.addControl(slider);
            return scene;
        };

        engine = createDefaultEngine();
        if (!engine) throw 'engine should not be null.';
        scene = createScene();;
        sceneToRender = scene

        engine.runRenderLoop(function () {
            if (sceneToRender) {
                sceneToRender.render();
            }
        });

        // Resize
        window.addEventListener("resize", function () {
            engine.resize();
        });
