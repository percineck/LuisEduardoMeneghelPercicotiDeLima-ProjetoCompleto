import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Group } from 'src/app/models/Group';

@Component({
  selector: 'app-internal-modal',
  templateUrl: './internal-modal.component.html',
  styleUrls: ['./internal-modal.component.css']
})
export class InternalModalComponent {
  @Input() title:string='';
  @Output() close = new EventEmitter(); 

  onClose(): void{
    this.close.emit(); 
  }
}
