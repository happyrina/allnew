const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];

let date = new Date();

let month = date.getMonth();
let year = date.getFullYear();

let daysInMonth = new Date(year, month + 1, 0).getDate();

let firstDay = new Date(year, month, 1).getDay();

document.getElementById("month").innerHTML = months[month];
document.getElementById("year").innerHTML = year;

let dates = "";
let day = 1;

for (let i = 0; i < 6; i++) {
    dates += "<tr>";
    for (let j = 0; j < 7; j++) {
        if (i === 0 && j < firstDay) {
            dates += "<td></td>";
        } else if (day > daysInMonth) {
            break;
        } else {
            if (day === date.getDate() && month === date.getMonth()) {
                dates += "<td class='today'>" + day + "</td>";
            } else {
                dates += "<td>" + day + "</td>";
            }
            day++;
        }
    }
    dates += "</tr>";
}

document.getElementById("dates").innerHTML = dates;
