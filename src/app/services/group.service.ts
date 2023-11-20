import { Injectable } from '@angular/core';
import { BaseApi } from './base.service';
import { Group } from '../models/Group';

@Injectable({
  providedIn: 'root'
})
export class GroupService {

  constructor(
    private _api: BaseApi,
  ) { }

  readAll(): Promise<Group[]>{
    return this._api.get(`group`);
  }


  readById(id: number): Promise<Group> {
    return this._api.get(`group/${id}`);
  }

  create(data: Partial<Group>): Promise<Group> {
    return this._api.post(`group`, data);
  }

  update(id: number, data: Partial<Group>):Promise<Group> {
    return this._api.post(`group/${id}`, data);
  }

  save(data: Partial<Group>): Promise<Group>{
    if (data?.id) return this.update(data.id, data);
    else return this.create(data);
  }

  delete(id: number): Promise<void> {
    return this._api.delete(`group/${id}`);
  } 
}