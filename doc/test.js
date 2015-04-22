/**
 * Created by lumiru on 17/04/15.
 */

var Client = require("node-rest-client").Client;

var args = {
    headers:{"Content-Type": "application/json"}
};

var client = new Client();

var host = "http://192.168.222.24:8080";

client.registerMethod("getToken", host + "/api-token-auth/", "POST");
client.registerMethod("root", host + "/", "GET");
client.registerMethod("getFlights", host + "/flights/", "GET");
client.registerMethod("getFlight", host + "/flights/${id}/", "GET");
client.registerMethod("getAvailableFlights", host + "/available_flights/", "GET");
client.registerMethod("getReservations", host + "/reservations/", "GET");
client.registerMethod("createReservation", host + "/reservation/", "PUT");
client.registerMethod("cancelReservation", host + "/reservation/${id}/cancel/", "POST");

client.methods.root(args, function (data,response){
    console.log("Root data:");
    console.log(data);
});
client.methods.getFlights(args, function (data,response){
    console.log("Full flights list:");
    console.log(data);

        var innerArgs = args;
        innerArgs.path = {
            id: data[0].pk
        };
    client.methods.getFlight(innerArgs, function (data, response) {
        console.log("First flight data:");
        console.log(data);
    });
});

var loginArgs = args;
loginArgs.data = {
    username: "john",
    password: "P@ssw0rd"
};
client.methods.getToken (args, function (data, response) {
    console.log("Get authentication token:")
    console.log(data);

    args.headers.Authorization = "Token " + data.token;
    console.log(args);
    client.methods.getReservations(args, function (data,response){
        console.log("Get reservations list:");
        console.log(data);
    });

    client.methods.getAvailableFlights(args, function (data,response){
        console.log("Available flights list:");
        console.log(data);

        var innerArgs = args;
        innerArgs.path = {
            id: data[0].pk
        };
        client.methods.getFlight(innerArgs, function (data, response) {
            console.log("First available flight data:");
            console.log(data);

            var resservationArgs = args;
            resservationArgs.data = {
                flight_id: data.pk,
                flight_class_id: data.classes[0].pk
            };
            client.methods.createReservation(resservationArgs, function (data,response) {
                console.log("Create reservation response:");
                var created = data.id;

                client.methods.getReservations(args, function (data,response){
                    console.log("Get reservations list:");
                    console.log(data);

                    delete args.data;
                    args.path = {
                        id: created
                    };
                    console.log(args);
                    client.methods.cancelReservation(args, function (data,response){
                        console.log("Cancel reservations response:");
                        console.log(data);

                        client.methods.getReservations(args, function (data,response){
                            console.log("Get reservations list:");
                            console.log(data);
                        });
                    });
                });
            });
        });
    });
});

