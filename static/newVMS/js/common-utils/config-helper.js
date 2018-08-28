/**
 * Gets the required configuration value and returns it as a Promise
 * @param {string} config_key Key for the configuration
 */
function get_config_promise(config_key) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: '/ajax/get_config/',
      type: 'POST',
      data: {
        'config_key': config_key,
        'method': 'GET'
      },
      error: function (err) {
        reject(err);
      },
      success: function (data) {
        let jsonData = JSON.parse(data);
        resolve(jsonData.result);
      }
    });
  });
}

/**
 * Sets the particular configuration in the Server
 * @param {String} config_key Key for the configuration
 * @param {String} config_value Value for the configuration
 */
function set_config_promise(config_key, config_value) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: '/ajax/get_config/',
      type: 'POST',
      data: {
        'config_key': config_key,
        'config_value': config_value,
        'method': 'SET'
      },
      error: function (err) {
        reject(err);
      },
      success: function (data) {
        let jsonData = JSON.parse(data);
        resolve(jsonData.result); // Should be a boolean value
      }
    });
  });
}