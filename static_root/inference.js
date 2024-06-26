alert("Increase your volume for sound feedback. Please confirm your acknowledgment to start.");
var currentStep = 1;
var totalSteps = {{ steps|length }};
var stepComponents = {
    {% for step in steps %}
        {{ step.order }}: [
            {% for component in step.components.all %}
                "{{ component }}",
            {% endfor %}
        ],
    {% endfor %}
};
var currentComponents
var countdownInterval;
var timeoutId;
var checkCount = 0;
var foundMatch;

$("#nextButton").click(goToNextStep);

function goToNextStep() {
    $("#nextButton").hide();
    $("#camera_src").show();
    startCamera()
    $("#checkButton").show();
    checkCount = 0;

    $(".step").removeClass("active-step");

    currentStep++;

    if (currentStep <= totalSteps) {
        console.log("next")
        $("#step" + currentStep).addClass("active-step");
    } else {
        // Redirect to home page
        console.log("home")
        window.location.href = "/";
    }
}

var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('camera_src');
var img = document.getElementById("client");
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var mode = true;
var mode_first = true;

video.width = 300;
video.height = 480;

// Scale the graph canvas accordingly to the window size
var widthupdate = window.innerWidth*0.1;
var heightupdate = window.innerHeight*0.4;

function setCanvasSize() {
    // Size configured as it will be sent to the server side
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    console.log(video.width + "x" + video.height); // Log canvas' width and height
}

function startCamera() {
    var samsung_camera = false
    var deviceId

    if (navigator.mediaDevices.getUserMedia) {
        var constraints = {
            video: {
                facingMode: 'environment'
            }
        };
        navigator.mediaDevices.enumerateDevices()
            .then(function(devices) {
                devices.forEach(function(device) {
                    if (device.kind === 'videoinput' && device.label.toLowerCase().includes('camera2 0, facing back')) {
                        deviceId = device.deviceId;
                        samsung_camera = true
                    }
                });
                if (samsung_camera) {
                    constraints.video.deviceId = { exact: deviceId };
                    console.log('device id ', deviceId);
                } else {
                    console.error('Camera "camera2 0, facing back" not found.');
                }
                navigator.mediaDevices.getUserMedia(constraints)
                    .then(function(stream) {
                        video.srcObject = stream;
                        video.setAttribute('autoplay', true);
                        video.play();
                    })
                    .catch(function(error) {
                        console.error('Error accessing camera:', error);
                    });
            })
            .catch(function(error) {
                console.error('Error enumerating devices:', error);
            });
    }
}

function Mode(){
    if (checkCount >= 5) {
        $("#nextButton").show();
    }
    if (mode == true){
        mode = false;
        checkCount++;
        var ws = new WebSocket(
            ws_scheme + '://' + window.location.host + '/'
        );
        ws.onopen = (event) => {
            console.log('WebSocket Connected!');
        };
        ws.onmessage = (event) => {
            var data = JSON.parse(event.data);
            console.log("HERES DATA", data)

            if ('detected_object_names' in data) {
                console.log("detected object names", data.detected_object_names)

                currentComponents = stepComponents[currentStep];
                console.log("components CURRENT", currentComponents)

                var detectedObjects = data.detected_object_names;

                foundMatch = currentComponents.every(component => detectedObjects.includes(component));
                frameUpdate = data.image;


                if (foundMatch){
                // startCamera()

                    img.src = "data:image/jpeg;base64," + frameUpdate;
                    ws.close();

                    var audioElement = document.getElementById('correctAudio');
                    audioElement.play();

                    if (currentStep === totalSteps) {
                        $("#nextButton").text("Done");
                    }

                    var title = document.getElementById("title"+currentStep);
                    if (title) {
                        title.style.color = 'green';
                        title.textContent += " ✅";
                    }

                    var whatyouneed = document.getElementById("whatyouneed"+currentStep);
                    if (whatyouneed) {
                        whatyouneed.textContent = "Great job! 👏";
                    }

                    $("#client").show();

                    console.log("Found match")

                    $("#checkButton").hide();

                    $("#nextButton").show();

                    stopMode()
                }
            } else {
            // frameUpdate = data.image;
            // img.src = "data:image/jpeg;base64," + frameUpdate;
            }
        };
        ws.onclose = (event) => {
            console.log('Close');
        };

        if (navigator.mediaDevices.getUserMedia) {
            var constraints = {
                video: {
                    facingMode: 'environment'
                }
            };

            var samsung_camera = false

            navigator.mediaDevices.enumerateDevices()
                .then(function(devices) {
                    devices.forEach(function(device) {
                        if (device.kind === 'videoinput' && device.label.toLowerCase().includes('camera2 0, facing back')) {
                            deviceId = device.deviceId;
                            samsung_camera = true
                        }
                    });

                    if (samsung_camera) {
                        constraints.video.deviceId = { exact: deviceId };
                        console.log('device id ', deviceId);
                    } else {
                        console.error('Camera "camera2 0" not found.');
                    }

                    navigator.mediaDevices.getUserMedia(constraints)

                        .then(function(stream) {
                            video.srcObject = stream;
                            video.setAttribute('autoplay', true);
                            video.play();

                            video.addEventListener('loadedmetadata', setCanvasSize);

                            var delay = 500; // adjust the delay to fit your needs (ms)
                            var jpegQuality = 0.6; // adjust the quality to fit your needs (0.0 -> 1.0)

                            setInterval(function() {
                                context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
                                canvas.toBlob(function(blob) {
                                    if (ws.readyState == WebSocket.OPEN) {
                                        if (mode == true){
                //   ws.send(new Uint8Array([]));
                                        } else {
                                            var reader = new FileReader();
                                            reader.readAsDataURL(blob);
                                            reader.onloadend = function() {
                                                var base64data = reader.result;

                    // Construct the message object with the Base64-encoded blob
                                                var message = {
                                                    image: base64data,
                                                    currentComponents: stepComponents[currentStep]
                                                };

                    // Convert the message to JSON string before sending
                                                ws.send(JSON.stringify(message));
                                            };
                                        }
                                    }
                                }, 'image/jpeg', jpegQuality);
                            }, delay);
                        });
                })
                .catch(function(error) {
                    console.error('Error enumerating devices:', error);
                });

        }
    }
    else if (mode == false){
        mode = true;
        console.log("STOPPED MODE, MODE IS", mode)
        stopMode()
    }
};

function enumerateDevices() {
    navigator.mediaDevices.enumerateDevices()
        .then(function(devices) {
            console.log("Devices:", devices);
        })
        .catch(function(err) {
            console.error("Error enumerating devices:", err);
        });
}

function stopMode() {
    clearTimeout(timeoutId);
    clearInterval(countdownInterval);

    // ws.close(); // Close the WebSocket connection

    if (!foundMatch){
        startCamera()
    } else {
        $("#camera_src").hide();
        console.log('ELEMENT hidden');
    }

    foundMatch = false;

    mode = true;
    // video.pause();
    // video.srcObject.getVideoTracks()[0].stop();
    // video.srcObject = null;

    $("#checkButton").text("Check");
    $("#countdownTimer").text("");
}

// Call the function to enumerate devices
startCamera();

$("#checkButton").click(function() {
    console.log("changing button MODE IS ", mode)
    Mode(); // Run the mode function immediately

    if (mode == true) {
        $(this).text("Check");
    } else {
        $(this).text("Cancel");

        var secondsLeft = 10; // Initial value for the countdown

        countdownInterval = setInterval(function() {
            secondsLeft--;
            $("#countdownTimer").text("Seconds left: " + secondsLeft);
            if (secondsLeft <= 0) {
                clearInterval(countdownInterval);
            }
        }, 1000); // Update the countdown every second, change text per 1 second
    }

    timeoutId = setTimeout(function() {
        if (!mode){
            Mode();
            $("#checkButton").text("Check");
            $("#countdownTimer").text("Times out").addClass("plus-sans fivehundred");;
            clearInterval(countdownInterval);
            openPopUp(currentStep) // To show the hints (if available)
            var audioElement = document.getElementById('errorAudio');
            audioElement.play();
        }
    },10000); // Time out in milliseconds, 10000ms = 10s
});

function openPopUp(currentStep) {
    document.getElementById("popup-box"+currentStep).style.display = "block";
}

function closePopUp(currentStep) {
    document.getElementById("popup-box"+currentStep).style.display = "none";
}