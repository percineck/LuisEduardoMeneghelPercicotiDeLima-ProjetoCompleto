import { BaseApi } from './base.service';
import { Contact } from '../models/Contact';
import { Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root'
})
export class ContactService {
  constructor(
    private _api: BaseApi,
  ) { }

  readAll(): Promise<Contact[]>{
    return this._api.get(`contact`);
  }


  readById(id: number): Promise<Contact> {
    return this._api.get(`contact/${id}`);
  }

  create(data: Partial<Contact>): Promise<Contact> {
    return this._api.post(`contact`, data);
  }

  update(id: number, data: Partial<Contact>):Promise<Contact> {
    return this._api.post(`contact/${id}`, data);
  }

  save(data: Partial<Contact>): Promise<Contact>{
    if (data?.id) return this.update(data.id, data);
    else return this.create(data);
  }

  delete(id: number): Promise<void> {
    return this._api.delete(`contact/${id}`);
  } 
}