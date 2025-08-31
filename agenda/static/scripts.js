let currentDate = new Date();

window.onload = function() {

    renderCalendar();
    
    document.getElementById("next").addEventListener("click", function() {
        const calendar = document.getElementById("calendar");
        calendar.innerHTML = ""; // Clear the calendar
        const mes = document.getElementById("mes");
        mes.innerHTML = ""; // Clear the month header
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    document.getElementById("prev").addEventListener("click", function() {
        const calendar = document.getElementById("calendar");
        calendar.innerHTML = ""; // Clear the calendar
        const mes = document.getElementById("mes");
        mes.innerHTML = ""; // Clear the month header
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

}

function renderCalendar() {
                const calendar = document.getElementById("calendar");
                const mes = document.getElementById("mes");
                const name = document.createElement("h1");

                const month = currentDate.getMonth(); // 0 for January, 1 for February, etc.
                const year = currentDate.getFullYear(); // Current year

                const daysInMonth = new Date(year, month + 1, 0).getDate();
                const firstDay = new Date(year, month, 1).getDay();
                
                name.textContent = currentDate.toLocaleString('default', { month: 'long' , year: 'numeric' });
                mes.appendChild(name);

                let day = 1;
                for (let i = 0; i < 6; i++) {
                    const row = document.createElement("tr");

                    for (let j = 0; j < 7; j++){
                        const cell = document.createElement("td");

                        if (i === 0 && j < firstDay){
                            cell.textContent = "";
                        } else if (day <= daysInMonth){
                            const form = document.createElement("form");
                            form.action = "/month";
                            form.method = "POST";
                            cell.appendChild(form);

                            const button = document.createElement("button");
                            const month = document.createElement("input");
                            const year = document.createElement("input");

                            month.type = "hidden";
                            month.name = "month";
                            month.value = currentDate.getMonth();

                            year.type = "hidden";
                            year.name = "year";
                            year.value = currentDate.getFullYear();

                            button.type = "submit";
                            button.textContent = day;
                            button.id = `day-${day}`;
                            button.name = "day";
                            button.value = day;

                            form.appendChild(month);
                            form.appendChild(year);
                            form.appendChild(button);

                            day++;
                        } else {
                            cell.textContent = "";
                        }

                        row.appendChild(cell);
                    }

                    calendar.appendChild(row);
                    if (day > daysInMonth) {
                        break;
                    }
                    }
                }

