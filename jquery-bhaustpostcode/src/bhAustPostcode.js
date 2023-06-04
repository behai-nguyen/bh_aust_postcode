/******************************************
 *
 * A JQuery plugin which enables searching for Australian postcodes 
 * based on locality aka suburb.
 *
 * The back-end this plugin uses is the web API written in Python.
 * The repo address is:
 *
 *   https://github.com/behai-nguyen/bh-aust-postcode 
 *
 * The UI library used is Bootstrap 5.0.
 *
 * @author          Be Hai Nguyen -- https://behainguyen.wordpress.com/
 * @copyright       Copyright (c) 2023 Be Hai Nguyen.
 *
 * @license         Dual licensed under the MIT and GPL licenses:
 *                  http://www.opensource.org/licenses/mit-license.php
 *                  http://www.gnu.org/licenses/gpl.html
 *
 * @github          https://github.com/behai-nguyen/bh-aust-postcode/jquery-bhaustpostcode
 * @version         1.0.0
 *
 ******************************************/
 
(function($) {
    'use strict';

    $.bhAustPostcode = {
		defaults: {
            // Postcode server URL.
            url: 'http://localhost:5000/api/v0/aust-postcode',

            // In millisecond. The wait time after the last keystroke
			// before initiating the AJAX search.
			keyStrokeDelay: 500,

            // User help. Note 500 millisecond! If overwrite keyStrokeDelay,
			// be sure to update this toolTip value also.
			toolTip: 
			    `<ul>
				    <li>Type 3 or more characters into locality to begin searching.</li>
					<li>By default, there's a 500 millisecond delay since the last keystroke when searching starts.</li>
					<li>Click on a result row to select locality, state and postcode.</li>
					<li>Press <b>ESC</b> to cancel current / close search result.</li>
					<li>If there were a previous selection, press <b>ESC</b> will reverse to this selection.</li>
					<li>Clear out locality and move away from it, will clear out state and postcode also.</li>
			    </ul>`,

			// See https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow#syntax
			// In rem. See Bootstrap's .form-control:focus:
			//    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
			//
			// 0.25rem is the spread-radius. At run-time, it seems to translate into
			// glowing width.
			//
			// The result panel should appear below this glowing border ( locality )
			// ( locality field ). At run-time, this value is calculated into pixel
			// equivalence to position the result panel.
			//
			// The proper solution is to calculate this "width" from from box-shadow,
			// but it appears too complicated. It is a TO_DO item.
			bootstrapEffectiveGlowWidth: 0.25,

			// In percent. The height of the result panel expressed
			// as a percent of the available viewport below locality,
			// state and postcode container.
			resultPanelHeight: 25,

            // The names and Ids of locality/suburb, state and
            // postcode fields.
            localityName: null,
            localityId: null,
            localityPlaceHolder: 'Please enter locality / suburb name...',
            stateName: null,
            stateId: null,
            postcodeName: null,
            postcodeId: null,
			
            // Bootstrap input group size. Available values: input-group-sm, 
            // input-group-lg or set to blank ( '' ) to use default size.
            bootstrapInputGroupSize: 'input-group-sm',

            // Feedback message when in error and no error message.
            errorMsg: 'Something has happened. Please check server.',

            // CSS theme -- see bhAustPostcode.css.
            theme: 'safe'
		}
    };

    function AustPostcode( el, options ) {
        this.$el = $( el );

        // Field group: locality, state and postcode.
        this.$austPostcode = null;
        // DOM locality field.
		this.$locality = null;
        // DOM state field.
		this.$state = null;
        // DOM postcode field.
		this.$postcode = null;

        // DOM Id of this.$resultPanel.
        this.resultPanelId = null;
		// DOM: Bootstrap 5.0 modal dialog to display result.
        this.$resultPanel = null;
		// DOM: this.$resultPanel main display area.
		this.$resultArea = null;

        this.options = options;
		this.options.url += this.options.url.endsWith( '/' ) ? '' : '/';

        this._generate();
    }

    AustPostcode.prototype = {
        _showResultPanel: function() {
			this.$resultPanel.removeClass( 'd-none' );
		},

        _hideResultPanel: function() {
			this.$resultPanel.addClass( 'd-none' );
		},

        _setValue: function( $elem, value ) {
			$elem.val( value );
			$elem.data( 'val', value );
		},

		_resetValue: function( $elem ) {
			$elem.val( '' );
			$elem.removeData( 'val' );
		},

		_resetAllFieldsValue() {
			this._resetValue( this.$locality );
			this._resetValue( this.$state );
			this._resetValue( this.$postcode );
		},

        _reverseAllFieldsValue() {
			this.$locality.val( this.$locality.data('val') );
			this.$state.val( this.$state.data('val') );
			this.$postcode.val( this.$postcode.data('val') );
		},

        _bindItemsEvent: function() {
			let _this = this;

            $( 'div.selector-item-entry', this.$resultArea ).on({
			    mouseenter: function( event ) {
				    $(this).removeClass('item-normal')
					    .addClass('item-highlight');
				},

                mouseleave: function( event ) {
				    $(this).removeClass('item-highlight')
					    .addClass('item-normal');
				},

				click: function( event ) {
			        _this._setValue( _this.$locality, $(this).attr('data-item-locality') );
			        _this._setValue( _this.$state, $(this).attr('data-item-state') );
			        _this._setValue( _this.$postcode, $(this).attr('data-item-postcode') );

					_this._hideResultPanel();
				}
			});
		},

        _doSearch: function( val ) {
			let searchURL = this.options.url + val;

			let _this = this;

			runAjaxEx( 'get', searchURL, {}, X_WWW_FORM_URLENCODED_UTF8, '' )
			    .then( function( data ) {
					let { status } = data;

					if ( status.status.code != OK ) return;

					_this.$resultArea.empty();

					status.data.localities.forEach( ( r ) => {
						var html = `<div class="row mt-1 selector-item-entry"
						                data-item-locality="${r.locality}"
										data-item-state="${r.state}"
										data-item-postcode="${r.postcode}">
										<div class="col-8">${r.locality}</div>
										<div class="col">${r.state}</div>
										<div class="col">${r.postcode}</div>
									</div>`;
						_this.$resultArea.append( $(html) );
					});

					_this._bindItemsEvent();

					_this._showResultPanel();
				}).
				catch( function( data ) {
				    let { xhr, error, errorThrown } = data;

                    let msg = errorThrown ? ( errorThrown.length > 0 )
					    : _this.options.errorMsg;

					new GenericDialog({ dialogId: '#errDlg',
					    title: 'For your info...', buttonClass: 'btn-danger',
					    bodyText: `<span><strong>${msg}</strong></span>`}).open();
				});
		},

		// Id for field group: locality, state and postcode.
        _assignResultDialogId: function() {
            var date = new Date();
			this.resultPanelId =
			    `id${date.getHours()}${date.getMinutes()}${date.getSeconds()}${date.getMilliseconds()}`;
        },

        _setResultAreaHeight: function() {
			var rect = this.$locality.get( 0 ).getBoundingClientRect();
			var height = ( window.innerHeight - rect.y - rect.height )
			             *( this.options.resultPanelHeight / 100 );
			this.$resultArea.css({ 'max-height': height, 'height': height });
        },

        _positionResultPanel: function() {
            let b = getBorderWidths( this.$resultPanel.get(0) );

			this.$resultPanel.width( this.$austPostcode.width() - b.l - b.r );
			var rect = this.$toolTip.get( 0 ).getBoundingClientRect();
			var $dialog = $( `#${this.resultPanelId}` );
			$dialog.css({top: Math.floor(rect.y + rect.height)
			            + convertRemToPixels(this.options.bootstrapEffectiveGlowWidth), 
						left: rect.x});
		},

        _createUIElements: function() {
			let opt = this.options;

			this._assignResultDialogId();

			this.$austPostcode =
				$( `<div class="bh-aust-postcode input-group ${opt.bootstrapInputGroupSize}">
						<span class="input-group-text postcode-tooltip">
							<span class="text-primary bi-question-circle-fill"
							    data-bs-toggle="tooltip" data-bs-placement="top" 
								data-bs-html="true" title="${opt.toolTip}"></span>
						</span>				
					    <input type="text" name="${opt.localityName}" id="${opt.localityId}"
					        placeholder="${this.options.localityPlaceHolder}"
					        class="form-control form-control-sm w-50 selector-input"
					        maxlength="32" autocomplete="off"/>
					    <input type="text" name="${opt.stateName}" id="${opt.stateId}"
					        class="form-control form-control-sm selector-input"
					        style="text-transform: uppercase;" maxlength="3" readonly
					        autocomplete="off"/>
					    <input type="text" name="${opt.postcodeName}" id="${opt.postcodeId}"
					        class="form-control form-control-sm selector-input"
					        maxlength="4" readonly autocomplete="off"/>
				</div>` );

            this.$toolTip = $( 'span.input-group-text.postcode-tooltip', this.$austPostcode );
			this.$locality = $( `#${opt.localityId}`, this.$austPostcode );
			this.$state = $( `#${opt.stateId}`, this.$austPostcode );
			this.$postcode = $( `#${opt.postcodeId}`, this.$austPostcode );

			this.$resultPanel =
				$(`<div id="${this.resultPanelId}"
				        class="bh-aust-postcode result-panel position-absolute d-none">
					    <div class="container"></div>
				</div>` );

            this.$resultArea = $( 'div.container', this.$resultPanel );

			// this.$el is the binding element itself.
			this.$el.append( this.$austPostcode );

			$( 'body' ).append( this.$resultPanel );

			this._setResultAreaHeight();

			this._positionResultPanel();
			var _this = this;
			$( window ).resize( () => { _this._positionResultPanel() });
			
			bindToolTipElements();
        },

        _setOptions: function () {
            var opt, func;

            for ( opt in this.options ) {
                func = 'set' + opt.charAt(0).toUpperCase() + opt.substring(1);

                if ( this[func] ) {
				    this.options[ opt ] = this.$el.attr( 'data-' + opt ) || this.options[ opt ];
                    this[ func ]( this.options[opt] );
                }
            }
        },

        _bindLocalityEvent: function() {
			let _this = this;

            $( `#${this.options.localityId}`, this.$austPostcode ).on({
			    keyup: delay( function(event) {
					if ( event.which == 27 ) {
						_this._reverseAllFieldsValue();
						_this._hideResultPanel();
						return;
					};

			        var val = $( event.target ).val();
			        if ( val.length < 3 ) return;

                    _this._doSearch( val );
			    }, this.options.keyStrokeDelay ),

                blur: function( event ) {
				    if ( _this.$locality.val() == 0 ) _this._resetAllFieldsValue();
				}
			});
		},

        _generate: function() {
			this._createUIElements();
			this._bindLocalityEvent();

			this._setOptions();

			this.init = true;
        },

        _destroy: function() {
            this.$austPostcode.remove();
            $.removeData( this.$el, 'bhAustPostcode' );
        },

		setTheme: function ( theme ) {
		    this.$austPostcode.attr( 'class', (this.$austPostcode.attr('class') || '')
			    .replace(/theme-.+\s|theme-.+$/, '') );
		    this.$resultPanel.attr( 'class', (this.$resultPanel.attr('class') || '')
			    .replace(/theme-.+\s|theme-.+$/, '') );
			this.$austPostcode.addClass( 'theme-' + theme );
		    this.$resultPanel.addClass( 'theme-' + theme );
		}
    };

    $.fn.bhAustPostcode = function( options, value ) {

        function get() {
            var bhAustPostcode = $.data(this, 'bhAustPostcode');

            if (!bhAustPostcode) {
                bhAustPostcode = new AustPostcode( this, $.extend(true, {}, options) );
                $.data(this, 'bhAustPostcode', bhAustPostcode);
            }

            return bhAustPostcode;
        }

		if ( typeof options === 'string' ) {
		    var bhAustPostcode,
			    values = [],
			    funcName = options.charAt(0).toUpperCase() + options.substring(1),
			    func = ( value !== undefined ? 'set' : 'get' ) + funcName,

			setOpt = function() {
				if ( bhAustPostcode[func] ) { bhAustPostcode[func].apply(bhAustPostcode, [value]); }
				if ( bhAustPostcode.options[options] ) { bhAustPostcode.options[options] = value; }
			},

			getOpt = function() {
				if ( bhAustPostcode[func] ) { return bhAustPostcode[func].apply(bhAustPostcode, [value]); }
				else if ( bhAustPostcode.options[options] ) { return bhAustPostcode.options[options]; }
				else { return undefined; }
			},

			runOpt = function () {
				bhAustPostcode = $.data( this, 'bhAustPostcode' );

				if ( bhAustPostcode ) {
				    if ( bhAustPostcode[options] ) { bhAustPostcode[options].apply(bhAustPostcode, [value]); }
				    else if ( value !== undefined ) { setOpt(); }
				    else { values.push( getOpt() ); }
				}
			};

		    this.each( runOpt );

		    return values.length ? (values.length === 1 ? values[0] : values) : this;
		}

        options = $.extend( {}, $.bhAustPostcode.defaults, options );

        return this.each( get );
    };

	$.fn.bhAustPostcode.defaults = $.bhAustPostcode.defaults;

}) (jQuery);