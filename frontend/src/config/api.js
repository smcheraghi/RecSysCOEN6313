import axios from 'axios'

export default () => {
  return axios.create({
    // baseURL: 'http://localhost:5000/api/',
    baseURL: 'http://localhost:3000/', // fake json server
    json: true
    // headers: {
    //   'Access-Control-Allow-Origin': '*',
    //   'Access-Control-Allow-Method': 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
    // }
  })
}
