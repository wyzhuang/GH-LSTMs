/*
 * The Apache Software License, Version 1.1
 *
 * Copyright (c) 2002 The Apache Software Foundation.  All rights
 * reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * 3. The end-user documentation included with the redistribution, if
 *    any, must include the following acknowlegement:
 *       "This product includes software developed by the
 *        Apache Software Foundation (http://www.apache.org/)."
 *    Alternately, this acknowlegement may appear in the software itself,
 *    if and wherever such third-party acknowlegements normally appear.
 *
 * 4. The names "The Jakarta Project", "Ant", and "Apache Software
 *    Foundation" must not be used to endorse or promote products derived
 *    from this software without prior written permission. For written
 *    permission, please contact apache@apache.org.
 *
 * 5. Products derived from this software may not be called "Apache"
 *    nor may "Apache" appear in their names without prior written
 *    permission of the Apache Group.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED.  IN NO EVENT SHALL THE APACHE SOFTWARE FOUNDATION OR
 * ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
 * USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 * ====================================================================
 *
 * This software consists of voluntary contributions made by many
 * individuals on behalf of the Apache Software Foundation.  For more
 * information on the Apache Software Foundation, please see
 * <http://www.apache.org/>.
 */
package org.apache.ant.antcore.execution;

import org.apache.ant.antcore.antlib.AntLibDefinition;
import org.apache.ant.antcore.antlib.ComponentLibrary;

/**
 * This class is used to maintain information about imports
 *
 * @author Conor MacNeill
 * @created 16 January 2002
 */
public class ImportInfo {
    /** the component library from which the import is made */
    private ComponentLibrary library;
    /** the library definition information */
    private AntLibDefinition libDefinition;

    /**
     * ImportInfo records what has been imported from an Ant Library
     *
     * @param library The library from which the import was made
     * @param libDefinition the library definition information
     */
    public ImportInfo(ComponentLibrary library,
                      AntLibDefinition libDefinition) {
        this.library = library;
        this.libDefinition = libDefinition;
    }

    /**
     * Get the classname that has been imported
     *
     * @return the classname that was imported.
     */
    public String getClassName() {
        return libDefinition.getClassName();
    }

    /**
     * Get the library from which the import was made
     *
     * @return the library from which the import was made
     */
    public ComponentLibrary getComponentLibrary() {
        return library;
    }

    /**
     * Get the type of the definition that was imported
     *
     * @return the type of definition
     */
    public int getDefinitionType() {
        return libDefinition.getDefinitionType();
    }

    /**
     * Get the name of the component within its library.
     *
     * @return the name of the component within its library
     */
    public String getLocalName() {
        return libDefinition.getDefinitionName();
    }

}
