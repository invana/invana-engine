"use strict";(self.webpackChunkgraphiql_ui=self.webpackChunkgraphiql_ui||[]).push([[594],{6594:function(e,r,n){n.r(r),n.d(r,{b:function(){return a}});var t=n(889),i=Object.defineProperty,o=function(e,r){return i(e,"name",{value:r,configurable:!0})};function l(e,r){return r.forEach((function(r){r&&"string"!==typeof r&&!Array.isArray(r)&&Object.keys(r).forEach((function(n){if("default"!==n&&!(n in e)){var t=Object.getOwnPropertyDescriptor(r,n);Object.defineProperty(e,n,t.get?t:{enumerable:!0,get:function(){return r[n]}})}}))})),Object.freeze(Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}))}o(l,"_mergeNamespaces");var f={exports:{}};!function(e){function r(r){return function(n,t){var i=t.line,l=n.getLine(i);function f(r){for(var o,f=t.ch,a=0;;){var u=f<=0?-1:l.lastIndexOf(r[0],f-1);if(-1!=u){if(1==a&&u<t.ch)break;if(o=n.getTokenTypeAt(e.Pos(i,u+1)),!/^(comment|string)/.test(o))return{ch:u+1,tokenType:o,pair:r};f=u-1}else{if(1==a)break;a=1,f=l.length}}}function a(r){var t,o,l=1,f=n.lastLine(),a=r.ch;e:for(var u=i;u<=f;++u)for(var s=n.getLine(u),c=u==i?a:0;;){var p=s.indexOf(r.pair[0],c),g=s.indexOf(r.pair[1],c);if(p<0&&(p=s.length),g<0&&(g=s.length),(c=Math.min(p,g))==s.length)break;if(n.getTokenTypeAt(e.Pos(u,c+1))==r.tokenType)if(c==p)++l;else if(!--l){t=u,o=c;break e}++c}return null==t||i==t?null:{from:e.Pos(i,a),to:e.Pos(t,o)}}o(f,"findOpening"),o(a,"findRange");for(var u=[],s=0;s<r.length;s++){var c=f(r[s]);c&&u.push(c)}for(u.sort((function(e,r){return e.ch-r.ch})),s=0;s<u.length;s++){var p=a(u[s]);if(p)return p}return null}}o(r,"bracketFolding"),e.registerHelper("fold","brace",r([["{","}"],["[","]"]])),e.registerHelper("fold","brace-paren",r([["{","}"],["[","]"],["(",")"]])),e.registerHelper("fold","import",(function(r,n){function t(n){if(n<r.firstLine()||n>r.lastLine())return null;var t=r.getTokenAt(e.Pos(n,1));if(/\S/.test(t.string)||(t=r.getTokenAt(e.Pos(n,t.end+1))),"keyword"!=t.type||"import"!=t.string)return null;for(var i=n,o=Math.min(r.lastLine(),n+10);i<=o;++i){var l=r.getLine(i).indexOf(";");if(-1!=l)return{startCh:t.end,end:e.Pos(i,l)}}}o(t,"hasImport");var i,l=n.line,f=t(l);if(!f||t(l-1)||(i=t(l-2))&&i.end.line==l-1)return null;for(var a=f.end;;){var u=t(a.line+1);if(null==u)break;a=u.end}return{from:r.clipPos(e.Pos(l,f.startCh+1)),to:a}})),e.registerHelper("fold","include",(function(r,n){function t(n){if(n<r.firstLine()||n>r.lastLine())return null;var t=r.getTokenAt(e.Pos(n,1));return/\S/.test(t.string)||(t=r.getTokenAt(e.Pos(n,t.end+1))),"meta"==t.type&&"#include"==t.string.slice(0,8)?t.start+8:void 0}o(t,"hasInclude");var i=n.line,l=t(i);if(null==l||null!=t(i-1))return null;for(var f=i;null!=t(f+1);)++f;return{from:e.Pos(i,l+1),to:r.clipPos(e.Pos(f))}}))}(t.a.exports);var a=l({__proto__:null,default:f.exports},[f.exports])}}]);
//# sourceMappingURL=594.186da959.chunk.js.map