import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Group } from 'src/app/models/Group';
import { GroupService } from 'src/app/services/group.service';
interface FormGroupData {
  name: FormControl;
}
@Component({
  selector: 'app-grupos',
  templateUrl: './grupos.component.html',
  styleUrls: ['./grupos.component.css']
})
export class GruposComponent {
  constructor(
    private formBuilder: FormBuilder,
    private groupService: GroupService,
  ) { 
    this.formGroup= this.formBuilder.group({
          name: ['', Validators.required],
        });
  }
  async loadGroups(){
    try {
      let obj;
      obj= await this.groupService.readAll()||[] as Group[];
      if(obj){
        this.groups=obj;
      }
    } catch (error) { }
  }
  async storeGroups(){
    localStorage.setItem('groups', JSON.stringify(this.groups));
  }
  async loadGroup(id:number){
    try {
      let obj;
      obj= await this.groupService.readById(id)as Group;
      if(obj){
        this.data=obj
      }
    } catch (error) { }
  }
  async ngOnInit() {
    await this.loadGroups();
    this.storeGroups();
  }
  @Input() groups: Group[] = [];
  @Output() close = new EventEmitter<any>(); 
  id?:number;
  data:Group=new Group();
  loading = true;
  submitting = false;
  formGroup: FormGroup<FormGroupData>;
  async save(){
    if (this.formGroup.valid) {
      this.submitting = true;
      const value = this.formGroup.value;
      Object.assign(this.data, value);
      await this.groupService.save(this.data);
      this.clean();
      this.loadGroups();
      this.storeGroups();
      this.submitting = false;
    } else alert('Verifique os campos antes de continuar!');
  }
  clean(){
    this.data=new Group();
    this.formGroup.reset();
  }
  editItem(id?:number){
    const index = this.groups.findIndex(c => c.id === id);
    if (id) {
      this.loadGroup(id);
      this.formGroup.patchValue(this.data);
    }
  }
  async deleteItem(id?:number){
    if (id) {
      this.groupService.delete(id!)
      this.loadGroups();
      this.storeGroups();
    }
    this.clean();
  }
  onClose(): void{
    this.close.emit(this.groups); 
  }
  get controls() {
    return this.formGroup.controls;
  }
}
