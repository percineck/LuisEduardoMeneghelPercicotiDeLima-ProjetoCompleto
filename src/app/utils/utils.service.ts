
import { CurrencyPipe, DatePipe } from "@angular/common";


export class UtilsService {

  constructor(
    private date: DatePipe,
  ) { }





  static transformTimestampToDate(obj: any): any {
    if (typeof obj === 'string' && Date.parse(obj) && new RegExp(/\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d(?:\.\d+)?Z?/).test(obj))
      return new Date(obj);

    if (null === obj || "object" !== typeof obj) return obj;

    if (obj instanceof Array) {
      const copy = [];
      for (let i = 0, len = obj.length; i < len; i++) {
        copy[i] = this.transformTimestampToDate(obj[i]);
      }
      return copy;
    }

    if (obj instanceof Object) {
      const copy: any = {};
      for (const attr in obj) {
        if (obj.hasOwnProperty(attr))
          copy[attr] = this.transformTimestampToDate(obj[attr]);
      }
      return copy;
    }

    throw new Error(
      "The object could not be transformed! Type is not supported."
    );
  }
}