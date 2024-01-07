var globalStartDate;
var globalEndDate;
var globalName;
var globalUserExists;

        /*
        This functions sends a request to the Python backend to check for the existence of a streamer
        with the name entered into the text input field with the id "sn". After the function receives an
        answer it will add some html to page to the inform the user of the result
        */
        checkStreamer = () =>
        {
            const button = document.getElementById('downloadButton')
            const name = document.getElementById('sn').value
            globalName = name;
            const urlname = name.split(" ").join("")
            const messageElement = document.getElementById('streamerCheck')

            if (name)
            {
                const url = "/index/check-streamer/" + urlname

                fetch(url)
                .then(response => response.json())
                .then(data => {
                    globalUserExists = data.streamer_exists
                    if (globalUserExists)
                    {
                        const message = "Streamer " + name + " exists"
                        messageElement.innerHTML = message
                        button.disabled = false;
                    }
                    else
                    {
                        const message = "Streamer " + name + " doesn't exist"
                        messageElement.innerHTML = message
                        button.disabled = true;
                    }

                })
            }
            else
            {
                messageElement.innerHTML = ''
                button.disabled = true;
            }
        }
        /*
        This function ensures endDate cannot be earlier than the startDate to prevent
        the upper bound (endDate) of our date range from being lower than the lower bound (startDate)
        */
        function validateDates()
        {
            const startDate = new Date(document.getElementById('start-date').value);
            const endDate = new Date(document.getElementById('end-date').value);
            const errorContainer = document.getElementById("errorContainer");

            // Check if the start date is before the end date
            if (startDate > endDate)
            {
                errorContainer.innerText = "Incorrect Date Ordering";
                errorContainer.style.color = "red";
                errorContainer.style.display = "block";
                return false; // Prevent form submission
            } else
            {
                errorContainer.style.display = "none";
            }
        }

        function toggler()
        {


            const startDate = new Date(document.getElementById('start-date').value);
            const endDate = new Date(document.getElementById('end-date').value);
            globalStartDate = startDate;
            globalEndDate = endDate
            const div = document.getElementById("loading");


            if(globalStartDate <= globalEndDate)
            {
                div.style.display = "block";
            }
            return false;
        }
        /*
        This function ensures the download button will be disabled unless the entire form has been filled
        out with valid inputs
        */
        function changeButton()
        {
            const button = document.getElementById('downloadButton')
            const startDate = new Date(document.getElementById('start-date').value);
            const endDate = new Date(document.getElementById('end-date').value);
            const name = document.getElementById('sn').value

            globalStartDate = startDate;
            globalEndDate = endDate

            if((globalStartDate <= globalEndDate) && globalUserExists)
            {

                button.disabled = false;
            }
            else
            {
                button.disabled = true;
            }
        }
        /*
        This function sets the value of the date input fields to give the range of the previous seven days
        startDate will the date 7 days prior to today and the endDate will be yesterday's date
        */
        function setLastWeek() {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        const yesterdayFormatted = yesterday.toISOString().split('T')[0];
        document.getElementById('end-date').value = yesterdayFormatted;

        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
        const sevenDaysAgoFormatted = sevenDaysAgo.toISOString().split('T')[0];
        document.getElementById('start-date').value = sevenDaysAgoFormatted;
        }
        /*
        This function sets the value of the date input fields to give the range of the previous month
        startDate will the the first of the previous month while endDate will the be last of the previous month
        */
        function setPreviousMonth() {
            const today = new Date();
            const lastMonthStart = new Date(today.getFullYear(), today.getMonth() - 1, 2);
            const lastMonthEnd = new Date(today.getFullYear(), today.getMonth());

            const lastMonthStartFormatted = lastMonthStart.toISOString().split('T')[0];
            const lastMonthEndFormatted = lastMonthEnd.toISOString().split('T')[0];

            document.getElementById('start-date').value = lastMonthStartFormatted;
            document.getElementById('end-date').value = lastMonthEndFormatted;
        }
        /*
        This function sets the value of the date input fields to give the range of the current month
        startDate will be set to the first of the month while the endDate will be set to today's date
        */
        function setThisMonth() {
            const today = new Date();
            const thisMonthStart = new Date(today.getFullYear(), today.getMonth(), 2);

            const thisMonthStartFormatted = thisMonthStart.toISOString().split('T')[0];
            const thisMonthEndFormatted = today.toISOString().split('T')[0];

            document.getElementById('start-date').value = thisMonthStartFormatted;
            document.getElementById('end-date').value = thisMonthEndFormatted;
        }
        /*
        Sets the date input fields to today's date when the window loads
        */
        window.onload = function() {
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('start-date').value = today;
            document.getElementById('end-date').value = today;
        }
