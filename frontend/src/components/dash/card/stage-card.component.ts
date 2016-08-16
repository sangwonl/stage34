import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { Stage } from '../../../models/stage';

import { TimeAgoPipe } from 'angular2-moment';

@Component({
    selector: 'stage-card',
    templateUrl: 'stage-card.component.html',
    styleUrls: ['stage-card.component.css'],
    pipes: [TimeAgoPipe]
})
export class StageCardComponent implements OnInit {
    @Input() stage: Stage;
    @Input() forNew: boolean = false;

    @Output() showInfo = new EventEmitter();
    @Output() toggleStatus = new EventEmitter();
    @Output() addNew = new EventEmitter();
    @Output() trash = new EventEmitter();

    constructor() {}

    ngOnInit() {}

    statusIconClass() {
        return {
            'fa-stop': this.stage.status == 'running',
            'fa-play': this.stage.status =='paused'
        }
    }

    canTrash() {
        return this.stage && this.stage.status == 'paused';
    }

    onInfoClicked() {
        this.showInfo.emit({value: this.stage});
    }

    onStatusClicked() {
        this.toggleStatus.emit({value: this.stage});
    }

    onNewClicked() {
        this.addNew.emit({});
    }

    onTrashClicked() {
        this.trash.emit({value: this.stage});
    }
}