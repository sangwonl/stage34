import { Component, OnInit, Input } from '@angular/core';

import { StageService } from '../../../services/stage.service';

import { Stage } from '../../../models/Stage';

import { TimeAgoPipe } from 'angular2-moment';

@Component({
    selector: 'stage-card',
    templateUrl: 'stage-card.component.html',
    styleUrls: ['stage-card.component.css'],
    providers: [StageService],
    pipes: [TimeAgoPipe]
})
export class StageCardComponent implements OnInit {
    @Input() stage: Stage;

    constructor(private stageService: StageService) {}

    ngOnInit() {}
}