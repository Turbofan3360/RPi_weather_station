self.data_length_dropdown.items = [
      ["1 hour", 1], ["2 hours", 2], ["3 hours", 3], ["6 hours", 6], ["12 hours", 12], ["1 day", 24], ["2 days", 48], ["3 days", 72]
    ]

        
    # Bringing down data list from the RPi
    def get_data(time_length):
      tries = 0
      while tries < 5:
        tries += 1
        data = anvil.server.call("return_data", time_length)

      if not data:
        raise ServerUnavailableError()
        
      return data

    # Processing the data
    def process_data(data):
     # Splitting the data list into a lists of timestamps, temperature and humidity
      timestamps = [i[0] for i in data]
      temperature_data = [i[1] for i in data]
      humidity_data = [i[2] for i in data]
      pressure_data = [i[3] for i in data]
      #Formatting the date/time strings
      for i in timestamps:
        i = datetime.strptime(i, "%d/%m/%y %H:%M")
      
      return timestamps, temperature_data, humidity_data, pressure_data

    # Functions to make graphs out of the data collected in functions above
    def graph_temperature(keys=None, event_name=None, sender=None):
      self.data_graph.layout.yaxis.title = "Temperature (°C)"
     # Making sure the graph axis are labeled correctly to go with the units the timestamps are in
      if self.data_length_dropdown.selected_value >= 3:
        self.data_graph.layout.xaxis.title = "Time since measurement taken (hours)"
      else:
        self.data_graph.layout.xaxis.title = "Time since measurement taken (minutes)"
        
      self.data_graph.layout.title = "Temperature:"
      self.data_graph.data = [graph_objects.Scatter(x = timestamps, y = temperature_data,)]

    def graph_humidity(keys=None, event_name=None, sender=None):
      self.data_graph.layout.yaxis.title = "Relative humidity (%)"
      # Making sure the graph axis are labeled correctly to go with the units the timestamps are in
      if self.data_length_dropdown.selected_value >= 3:
       self.data_graph.layout.xaxis.title = "Time since measurement taken (hours)"
      else:
        self.data_graph.layout.xaxis.title = "Time since measurement taken (minutes)"
        
      self.data_graph.layout.title = "Humidity:"
      self.data_graph.data = [graph_objects.Scatter(x = timestamps, y = humidity_data, marker=dict(color="rgb(255, 17, 0)"))]

    def graph_pressure(keys=None, event_name=None, sender=None):
      self.data_graph.layout.yaxis.title = "Air pressure (hPa/mbar)"
      # Making sure the graph axis are labeled correctly to go with the units the timestamps are in
      if self.data_length_dropdown.selected_value >= 3:
        self.data_graph.layout.xaxis.title = "Time since measurement taken (hours)"
      else:
        self.data_graph.layout.xaxis.title = "Time since measurement taken (minutes)"
        
      self.data_graph.layout.title = "Air pressure:"
      self.data_graph.data = [graph_objects.Scatter(x = timestamps, y = pressure_data, marker=dict(color="rgb(255, 255, 51)"))]

    def data_length_change(event_name=None, sender=None):
      time_length = self.data_length_dropdown.selected_value * 3600
      try:
        data = get_data(time_length)
      except ServerUnavailableError:
        alert(title="Server currently unavailable: Please try reloading webpage", dismissible=False)
      
      global timestamps, temperature_data, humidity_data, pressure_data
      timestamps, temperature_data, humidity_data, pressure_data = process_data(data)
      
      # Setting the current temperature and humidity to be the latest (i.e. first) values in the lists
      current_temperature = temperature_data[0]
      current_humidity = humidity_data[0]
      current_pressure = pressure_data[0]
     # Making the two lines of text at the top display the current humidity/temperature
      self.current_temperature.content = "Current temperature:  {}°C".format(current_temperature)
      self.current_humidity.content = "Current humidity:  {}%".format(current_humidity)
      self.current_pressure.content = "Current air pressure:   {} hPa/mbar".format(current_pressure)
      
      graph_temperature()
      
      
    # Setting a couple of defaults
    Plot.templates.default = "rally"
    self.data_graph.interactive = False

    # Getting and processing the data from the Pi using functions defined above
    try:
      data = get_data(3600)
    except ServerUnavailableError:
      alert(title="Server unavailable: Please try reloading webpage", dismissible=False)
      exit()
      
    global timestamps, temperature_data, humidity_data, pressure_data
    timestamps, temperature_data, humidity_data, pressure_data = process_data(data)
    
   # Setting the current humidity/temperature to be the latest value (i.e. first value) in the data list sent down
    current_humidity = humidity_data[0]
    current_temperature = temperature_data[0]
    current_pressure = pressure_data[0]
    
    # Making the two lines of text at the top display the current humidity/temperature
    self.current_temperature.content = "Current temperature:  {}°C".format(current_temperature)
    self.current_humidity.content = "Current humidity:  {}%".format(current_humidity)
    self.current_pressure.content = "Current air pressure:   {} hPa/mbar".format(current_pressure)
      
    # Automatically sets that graph to show temperature data
    graph_temperature()

    # Set event handlers to run functions when certain buttons are pressed
    self.humidity.set_event_handler("click", graph_humidity)
    self.temperature.set_event_handler("click", graph_temperature)
    self.pressure.set_event_handler("click", graph_pressure)
    self.data_length_dropdown.set_event_handler("change", data_length_change)
