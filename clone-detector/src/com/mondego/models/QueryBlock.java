/**
 * 
 */
package com.mondego.models;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import com.mondego.indexbased.SearchManager;
import com.mondego.utility.BlockInfo;

/**
 * @author vaibhavsaini
 *
 */
public class QueryBlock {
    private long id; // file id
    private int size;  // num tokens
    private long functionId; // project id
    private int prefixSize;
    private int computedThreshold;
    private int maxCandidateSize;
    private int numUniqueTokens;
    private String projectName;
    private String fileName;
    private int startLine;
    private int endLine;
    private List<Double> metrics;
    private String fqmn;
    private long rowId;

    /**
     * @param id
     * @param size
     */
    public QueryBlock(String rawQuery) {
        this.populateMetrics(rawQuery);
        
    }

    public void populateMetrics(String rawQuery){
    	// 465632~~selected_2351875.org.lnicholls.galleon.togo.ToGo.clean(String)~~selected~~2351875.java~~750~~763~~40~~6~~13~~10009103025115~~1~~0~~13~~109~~24~~6173.52~~0.17~~1~~1~~0~~14~~0~~1~~1~~12.35~~0~~0~~0~0~~0~~499.76~~60~~23~~49~~0~~22~~0
    	
    	
    	String[] columns = rawQuery.split("~~");
    	this.rowId = Long.parseLong(columns[0]);
    	this.fqmn = columns[1];
    	this.projectName= columns[2];
    	this.fileName = columns[3];
    	this.startLine = Integer.parseInt(columns[4]);
    	this.endLine = Integer.parseInt(columns[5]);
    	this.size = Integer.parseInt(columns[6]);
    	this.numUniqueTokens = Integer.parseInt(columns[7]);
    	this.functionId = Integer.parseInt(columns[8]);
    	this.id = Integer.parseInt(columns[9]);
    	this.metrics = new ArrayList<Double>();
    	for (int i=10;i<columns.length;i++){
    		this.metrics.add(Double.parseDouble(columns[i]));
    	}
    	this.computedThreshold = BlockInfo
                .getMinimumSimilarityThreshold(this.numUniqueTokens, SearchManager.th);
        this.setMaxCandidateSize(BlockInfo
                .getMaximumSimilarityThreshold(this.numUniqueTokens, SearchManager.th));
        this.prefixSize = BlockInfo.getPrefixSize(this.numUniqueTokens,
                this.computedThreshold);
    }
    /**
     * @return the id
     */
    public long getId() {
        return id;
    }

    /**
     * @param id
     *            the id to set
     */
    public void setId(long id) {
        this.id = id;
    }

    public long getFunctionId() {
        return functionId;
    }

    public void setFunctionId(long functionId) {
        this.functionId = functionId;
    }

    public int getPrefixSize() {
        return prefixSize;
    }

    public void setPrefixSize(int prefixSize) {
        this.prefixSize = prefixSize;
    }

    public int getComputedThreshold() {
        return computedThreshold;
    }

    public void setComputedThreshold(int computedThreshold) {
        this.computedThreshold = computedThreshold;
    }

    public int getMaxCandidateSize() {
        return maxCandidateSize;
    }

    public void setMaxCandidateSize(int maxCandidateSize) {
        this.maxCandidateSize = maxCandidateSize;
    }

    @Override
    public String toString() {
        return this.getFunctionId() + "," + this.getId() + "," + this.getSize() + ","+ this.getNumUniqueTokens();
    }

    private long getSize() {
		return this.size;
	}

	/**
     * @return the numUniqueTokens
     */
    public int getNumUniqueTokens() {
        return numUniqueTokens;
    }

    /**
     * @param numUniqueTokens
     *            the numUniqueTokens to set
     */
    public void setNumUniqueTokens(int numUniqueTokens) {
        this.numUniqueTokens = numUniqueTokens;
    }
}
