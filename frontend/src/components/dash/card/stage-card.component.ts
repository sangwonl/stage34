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

    @Output() toggleStatus = new EventEmitter();
    @Output() showInfo = new EventEmitter();
    @Output() addNew = new EventEmitter();
    @Output() trash = new EventEmitter();

    constructor() {}

    ngOnInit() {}

    private statusIconClass() {
        return {
            'fa-spinner fa-pulse fa-fw': ['creating', 'changing'].includes(this.stage.status),
            'fa-stop': this.stage.status === 'running',
            'fa-play': this.stage.status ==='paused'
        }
    }

    private canTrash() {
        return this.stage && this.stage.status === 'paused';
    }

    private onInfoClicked() {
        this.showInfo.emit({value: this.stage});
    }

    private onStatusClicked() {
        if (['running', 'paused'].includes(this.stage.status)) {
            this.toggleStatus.emit({value: this.stage});
        }
    }

    private onNewClicked() {
        this.addNew.emit({});
    }

    private onTrashClicked() {
        this.trash.emit({value: this.stage});
    }
}