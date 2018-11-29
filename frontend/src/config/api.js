import axios from 'axios'

export default () => {
  return axios.create({
    baseURL: 'https://rec.wannaseethat.tk/api/',
    // baseURL: 'http://localhost:3000/',
    json: true,
    // headers: {
    //   'Access-Control-Allow-Origin': '*',
    //   'Access-Control-Allow-Method': 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
    // }
  })
}
