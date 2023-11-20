import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';


import { UtilsService } from '../utils/utils.service';



@Injectable({
  providedIn: 'root'
})
export class BaseApi {

  protected host = 'http://ec2-18-117-167-148.us-east-2.compute.amazonaws.com:3000';
  constructor(
    protected http: HttpClient,
  ) { }

  async get(endpoint: String, params?: any, reqOpts?: {headers: HttpHeaders, params?: HttpParams}): Promise<any> {
   

    if (!reqOpts) {
      reqOpts = {
        headers: this.getHeaders,
        params: new HttpParams()
      }
    }

    if (params) {
      reqOpts.params = new HttpParams();
      for (let k in params) {
        reqOpts.params = reqOpts.params.set(k, params[k]);
      }
    }

    return new Promise((resolve, reject) => {
      this.http.get(`${this.host}/${endpoint}`, reqOpts).subscribe(res => {
        const result = UtilsService.transformTimestampToDate(res);
        resolve(result);
      }, err => {
        reject(err);
      })
    })
  }

  async post(endpoint: String, data: Object, reqOpts?: {headers: HttpHeaders}): Promise<any> {
    

    if (!reqOpts) {
      reqOpts = {
        headers: this.getHeaders
      }
    }

    return new Promise((resolve, reject) => {
      this.http.post(`${this.host}/${endpoint}`, data, reqOpts).subscribe(res => {
        const result = UtilsService.transformTimestampToDate(res);
        resolve(result);
      }, err => {
        reject(err);
      })
    })
  }

  async put(endpoint: String, data: Object, reqOpts?: {headers: HttpHeaders}): Promise<any> {
    

    if (!reqOpts) {
      reqOpts = {
        headers: this.getHeaders
      }
    }

    return new Promise((resolve, reject) => {
      this.http.put(`${this.host}/${endpoint}`, data, reqOpts).subscribe(res => {
        const result = UtilsService.transformTimestampToDate(res);
        resolve(result);
      }, err => {
        reject(err);
      })
    })
  }

  async patch(endpoint: String, data?: Object, reqOpts?: {headers: HttpHeaders}): Promise<any> {
    

    if (!reqOpts) {
      reqOpts = {
        headers: this.getHeaders
      }
    }

    return new Promise((resolve, reject) => {
      this.http.patch(`${this.host}/${endpoint}`, data, reqOpts).subscribe(res => {
        const result = UtilsService.transformTimestampToDate(res);
        resolve(result);
      }, err => {
        reject(err);
      })
    })
  }

  async delete(endpoint: String, data?: Object, reqOpts?: {headers: HttpHeaders, body?: Object}): Promise<any> {
    

    if (!reqOpts) {
      reqOpts = {
        headers: this.getHeaders
      }
    }
    if (data) reqOpts.body = data;

    return new Promise((resolve, reject) => {
      this.http.delete(`${this.host}/${endpoint}`, reqOpts).subscribe(res => {
        const result = UtilsService.transformTimestampToDate(res);
        resolve(result);
      }, err => {
        reject(err);
      })
    })
  }

  protected get getHeaders() {
   
   
      return new HttpHeaders()
      .append('accept', 'application/json')
      .append('Content-Type', 'application/json')
      ;
  }

  convertToFormData(data: any) {
    const formData = new FormData();

    Object.keys(data).forEach(name => {
      const val = data[name];

      if (val instanceof Array) {
        val.forEach((val2, i) => {
          const formData2 = this.convertToFormData(val2);

          formData2.forEach((value, key) => {
            formData.append(`${name}[${i}]${key}`, value);
          });
        });
      } else formData.append(name, val);
    });

    return formData;
  }
  
}