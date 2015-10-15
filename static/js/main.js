window.onload = function () {
    var cars = document.querySelectorAll('.all-cars')[0].querySelectorAll('.cars');
    var parkedCars = document.querySelectorAll('.parked-cars')[0].querySelectorAll('.cars');
    var form = document.getElementsByTagName('form')[0];
    var carId = document.getElementById('id');
    var carAction = document.getElementById('car-action');
    var addParkingButtton = document.getElementById('add-car');
    var removeParkingButtton = document.getElementById('remove-car');

    for (var i = 0; i < cars.length; i++) {
        var car = cars[i];
        if (car.getAttribute('parked') === "False") {
            car.addEventListener('click', function (event) {
                clearActiveCars();
                var target = event.target;
                target.classList.add("active");
                carId.value = target.getAttribute('src');
                carAction.value = "park"
                addParkingButtton.disabled = false;
                removeParkingButtton.disabled = true;
            })
        } else {
            car.classList.add("inactive");
        }
    }

    for (var j = 0; j < parkedCars.length; j++) {
        var parkedCar = parkedCars[j];
        parkedCar.addEventListener('click', function (event) {
            clearActiveCars();
            var target = event.target;
            target.classList.add("active");
            carId.value = target.getAttribute('license-plate');
            carAction.value = "remove";
            addParkingButtton.disabled = true;
            removeParkingButtton.disabled = false;
            getCarInfo(carId.value)
        })
    }

    function getCarInfo(plate) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var data = JSON.parse(xhttp.responseText);
                console.log(data)
                var image = data['image_path']
                var html_image = "<img src='" + image + "'/>"
                var register = new Date(parseInt(data['register_time'])*1000)
                var html = "STATUS: " + data.status + "<br> registered parking time:" +  register;
                document.getElementById("result_image").innerHTML = html_image;
                document.getElementById("result").innerHTML = html;


            }
        };
        xhttp.open("GET", "http://127.0.0.1:666/car/" + plate, true);
        xhttp.send();
    }

    function clearActiveCars() {
        var cars = document.querySelectorAll('.cars');
        for (var i = 0; i < cars.length; i++) {
            var car = cars[i];
            car.classList.remove('active')
        }
    }


};