
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'zeroPadding'
})
export class ZeroPaddingPipe implements PipeTransform {
  transform(value?: number): string {
    if(value){
        if (isNaN(value) || value < 0) {
            return '';
        }
        const stringValue = value.toString();
        if (stringValue.length === 1) {
        return '00' + stringValue;
        } else if (stringValue.length === 2) {
        return '0' + stringValue;
        } else {
        return stringValue;
        }
    }
    return '';
  }
}
